# Product Listing: Stainless Steel Water Bottle

## Product overview

**Product name:** Stainless Steel Water Bottle  
**Selling price:** ₹289  
**Recipient for email draft:** cheerarohan@gmail.com

A sleek, reusable water bottle with a polished silver finish and a screw-on cap. Its cylindrical design makes it suitable for everyday hydration at home, at work, at college, or while travelling.

## Details observed in the photos

- **Colour:** Silver
- **Appearance:** Reflective, polished metal finish
- **Shape:** Tall cylindrical body
- **Closure:** Screw-on cap
- **Price provided:** ₹289

### Details that are not verified

- **Material/grade:** It appears to be stainless steel, but the exact material grade is not visible.
- **Capacity:** Not provided; do not guess the volume.
- **Insulation:** Not established by the photos.
- **Leak resistance:** Not tested or verified.
- **Brand:** Not visible.

## Suggested product title

**Stainless Steel Water Bottle – Silver Finish | ₹289**

## Suggested selling description

Stay hydrated throughout your day with this sleek silver-finish water bottle. Featuring a simple cylindrical design and screw-on cap, it is suitable for everyday use at home, in the office, at college, or while travelling. Its reflective finish gives it a clean, classic look.

**Price: ₹289**

*Please confirm the capacity, material grade, and whether it is insulated before publishing those specifications.*

## Email draft

**To:** cheerarohan@gmail.com  
**Subject:** Product Listing – Stainless Steel Water Bottle | ₹289

Hi,

Please find the product listing details below.

**Product Name:** Stainless Steel Water Bottle  
**Price:** ₹289

**Description:**  
A sleek, reusable water bottle with a polished silver finish and screw-on cap. Its cylindrical design makes it suitable for everyday use at home, in the office, at college, or while travelling.

**Specifications:**
- Colour: Silver
- Appearance: Polished, reflective finish
- Closure: Screw-on cap
- Capacity: Not specified
- Material grade: Not verified
- Insulation: Not verified

**Suggested Selling Title:** Stainless Steel Water Bottle – Silver Finish | ₹289

Regards

---

## Automating this workflow with a Custom GPT

The intended workflow is:

1. The user uploads one or more product photos and provides the selling price.
2. The Custom GPT analyzes visible features and generates a product title, description, and structured details.
3. The Custom GPT calls a configured GPT Action that sends the generated content to a backend endpoint.
4. The backend validates the request and sends the email through an email provider such as Resend or Amazon SES.

### Example API request

```json
{
  "to": "cheerarohan@gmail.com",
  "subject": "Product Listing – Stainless Steel Water Bottle | ₹289",
  "product_name": "Stainless Steel Water Bottle",
  "price_inr": 289,
  "description": "A sleek, reusable water bottle with a polished silver finish and screw-on cap. Suitable for everyday use at home, in the office, at college, or while travelling.",
  "specifications": {
    "colour": "Silver",
    "closure": "Screw-on cap",
    "capacity": null,
    "material_grade": "Unverified",
    "insulation": "Unverified"
  }
}
```

### Implementation checklist

- Create a backend endpoint, for example `POST /send-product-email`.
- Validate recipient addresses and input fields on the backend.
- Connect an email provider and configure its API key as a server-side secret.
- Define the endpoint in the Custom GPT's Action OpenAPI schema.
- Restrict access with authentication; do not expose provider API keys in the GPT instructions or client code.
- Return a clear success or failure result from the backend.
- Decide whether emails should be sent automatically or only after a separate confirmation step.

**Status:** This file documents the product response and proposed integration. No email has been sent by creating this file.
