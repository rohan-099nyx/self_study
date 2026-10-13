import base64
import json
import os
import re
import secrets
from datetime import datetime, timezone
from typing import Any
from urllib.parse import quote

import requests
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, HttpUrl, field_validator

app = FastAPI(
    title="Product Gig to GitHub API",
    description="Accepts a generated product gig and saves it as a JSON file in GitHub.",
    version="1.0.0",
)

ACTION_API_KEY = os.getenv("ACTION_API_KEY", "")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "rohan-099nyx/self_study")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
GITHUB_DIR = os.getenv("GITHUB_DIR", "product-gigs")


class ProductGig(BaseModel):
    product_name: str = Field(min_length=1, max_length=160)
    category: str = Field(default="General", max_length=100)
    price: float | None = Field(default=None, ge=0)
    currency: str = Field(default="INR", min_length=3, max_length=3)
    short_title: str = Field(min_length=1, max_length=200)
    description: str = Field(min_length=1, max_length=5000)
    highlights: list[str] = Field(default_factory=list, max_length=20)
    specifications: dict[str, Any] = Field(default_factory=dict)
    image_links: list[HttpUrl] = Field(default_factory=list, max_length=20)
    image_notes: list[str] = Field(default_factory=list, max_length=20)
    social_posts: dict[str, str] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list, max_length=30)
    email_subject: str | None = Field(default=None, max_length=200)
    email_body: str | None = Field(default=None, max_length=10000)
    source_notes: list[str] = Field(default_factory=list, max_length=30)

    @field_validator("image_links")
    @classmethod
    def require_https_image_links(cls, value):
        for url in value:
            if url.scheme != "https":
                raise ValueError("Image links must use HTTPS.")
        return value


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return (slug[:70] or "product-gig")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "product-gig-github-api"}


@app.post("/products", status_code=201)
def save_product_gig(
    gig: ProductGig,
    x_action_key: str | None = Header(default=None, alias="X-Action-Key"),
):
    if not ACTION_API_KEY or not secrets.compare_digest(x_action_key or "", ACTION_API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing Action API key.")
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=503, detail="GitHub integration is not configured.")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", GITHUB_REPO):
        raise HTTPException(status_code=500, detail="GITHUB_REPO must be in owner/repo format.")

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")
    filename = f"{slugify(gig.product_name)}-{timestamp}-{secrets.token_hex(3)}.json"
    path = f"{GITHUB_DIR.strip('/')}/{now.strftime('%Y/%m')}/{filename}"
    payload = gig.model_dump(mode="json")
    payload["saved_at"] = now.isoformat()
    payload["repository"] = GITHUB_REPO
    payload["schema_version"] = "1.0"

    encoded_content = base64.b64encode(
        json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("ascii")
    safe_path = quote(path, safe="/")
    endpoint = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{safe_path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    body = {
        "message": f"Add product gig: {gig.product_name[:72]}",
        "content": encoded_content,
        "branch": GITHUB_BRANCH,
    }

    try:
        response = requests.put(endpoint, headers=headers, json=body, timeout=20)
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Could not reach GitHub.")

    if response.status_code not in (200, 201):
        # Do not return provider response bodies, which may contain implementation details.
        raise HTTPException(
            status_code=502,
            detail=f"GitHub could not save the product gig (HTTP {response.status_code}).",
        )

    result = response.json()
    html_url = result.get("content", {}).get("html_url")
    commit_sha = result.get("commit", {}).get("sha")
    return {
        "status": "saved",
        "message": "Product gig JSON committed to GitHub.",
        "repository": GITHUB_REPO,
        "path": path,
        "file_url": html_url,
        "commit_sha": commit_sha,
        "saved_at": payload["saved_at"],
    }
