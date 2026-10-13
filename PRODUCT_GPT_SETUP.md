# Custom GPT: Product Gig Creator → GitHub JSON

This setup uses a small secured API. Each time your Custom GPT processes a product, it can save a fresh JSON file to this repository.

## What it does

1. You upload product photos and provide any known details (price, brand, capacity, target audience, etc.).
2. The GPT writes a product gig: title, listing description, highlights, specs, image links, and social captions.
3. The GPT calls `POST /products` on your API.
4. The API commits one JSON file under `product-gigs/YYYY/MM/` in this repository and returns the file URL.

**Image-link limitation:** an image attached to a ChatGPT conversation does not automatically become a public HTTPS URL. Include public image links only when you provide them or the GPT can verify them. Otherwise keep `image_links` empty and explain that the photo needs hosting before it can be linked publicly. Never fabricate image URLs or unsupported product specifications.

## Files

- `product_gig_api/main.py`: FastAPI service that validates the action key and commits the product JSON to GitHub.
- `product_gig_api/requirements.txt`: Python dependencies.
- `product_gig_api/render.yaml`: starter Render deployment blueprint.
- `product_gig_api/openapi.yaml`: schema to paste into the GPT Action editor after replacing the server URL.

## 1. Deploy the API

1. Open Render and choose **New → Blueprint** (or create a Python web service).
2. Connect this repository, `rohan-099nyx/self_study`.
3. If using the Blueprint route, set the blueprint file path to `product_gig_api/render.yaml` if the Render UI supports specifying a non-root blueprint path. Otherwise create a Web Service manually with root directory `product_gig_api`, build command `pip install -r requirements.txt`, start command `uvicorn main:app --host 0.0.0.0 --port $PORT`, and health-check path `/`.
4. Add environment variables in Render:
   - `ACTION_API_KEY`: a long random secret that you generate.
   - `GITHUB_TOKEN`: a GitHub fine-grained personal access token restricted to this repository, with **Contents: Read and write** permission.
   - `GITHUB_REPO`: `rohan-099nyx/self_study`
   - `GITHUB_BRANCH`: `main`
   - `GITHUB_DIR`: `product-gigs`
5. Deploy and copy the HTTPS service URL. Test `https://YOUR-API-URL/`; it should return `{"status":"ok","service":"product-gig-github-api"}`.

Keep both secrets in Render's environment settings. Never put the GitHub token in the GPT instructions, OpenAPI schema, or repository.

## 2. Configure your Custom GPT

In ChatGPT, open **Explore GPTs → Create**. In Configure:

- **Name:** Product Gig Creator
- **Description:** Turns product photos and details into listing copy, image links, social posts, and a JSON record saved to GitHub.
- Enable image understanding / vision if available. Enable web search if you want it to discover publicly accessible reference image links.
- Under **Actions**, create an action and paste the content of `product_gig_api/openapi.yaml`. Replace `https://YOUR-DEPLOYED-API.onrender.com` with your deployed service URL.
- In the Action authentication settings choose **API Key**, header authentication, header name `X-Action-Key`, and enter the same `ACTION_API_KEY` value configured on the server.
- Save and test the GPT.

## 3. Paste this into the GPT Instructions

You are Product Gig Creator. For every product the user asks you to process:

1. Analyze all product photos and user-provided details. Produce a useful commercial product gig with:
   - product name and category
   - concise sales title
   - clear marketing description
   - price and currency when supplied
   - highlights and structured specifications
   - image links
   - platform-specific social copy (Instagram, Facebook, WhatsApp)
   - tags
   - email subject/body when useful
   - source notes listing unknown or unverified details
2. Never infer exact dimensions, capacity, brand, material grade, certifications, warranty, health claims, or performance claims from appearance alone. Mark unknown values as unknown or leave them out. Preserve the user's exact price.
3. For image_links, use only HTTPS image URLs supplied by the user or URLs you can verify through browsing. Do not fabricate URLs. Do not pretend an uploaded local attachment already has a public URL. When no public image URL is available, use an empty array and explain that hosting is needed.
4. Always return the generated gig to the user in readable form, and include the JSON record structure used for saving.
5. After generating a valid gig, call the `saveProductGigToGitHub` Action exactly once to persist it. Do not ask for a separate confirmation unless the user says not to save. If required fields are missing, make conservative assumptions and clearly record unknowns rather than repeatedly questioning the user.
6. If the Action succeeds, show the returned GitHub file URL and path. If it fails, explain that it was not saved and do not claim success.
7. Do not expose or repeat secrets.

## 4. Example user message

"Create a product gig from these photos. Price ₹289. Save the JSON to GitHub."

## 5. Test result expectations

The action response should include `status: saved`, a repository path such as `product-gigs/2026/10/stainless-steel-water-bottle-....json`, and a direct GitHub file URL. Verify the created file in the repository after your first test.

## API request shape

See `openapi.yaml` for the full schema. The backend creates a timestamped, unique JSON filename so repeated uses do not overwrite previous product gigs.
