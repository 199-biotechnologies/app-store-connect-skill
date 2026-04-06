# Customer Reviews & Ratings

Manage customer reviews: read, respond, delete responses, and use AI-assisted drafting.

## List Customer Reviews

```python
# List all reviews for an app (newest first, filter by rating)
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/customerReviews",
    headers=headers,
    params={
        "sort": "-createdDate",
        "limit": 50
    }
)
reviews = response.json()['data']
for review in reviews:
    attrs = review['attributes']
    print(f"[{attrs['rating']}*] {attrs.get('title', 'No title')}: {attrs['body'][:100]}")
```

### Filter by Rating

```python
# Only 1-2 star reviews (critical to respond to)
params = {"sort": "-createdDate", "filter[rating]": "1,2", "limit": 50}

# Only 4-5 star reviews
params = {"sort": "-createdDate", "filter[rating]": "4,5", "limit": 50}
```

### Reviews for a Specific Version

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{VERSION_ID}/customerReviews",
    headers=headers,
    params={"sort": "-createdDate", "limit": 20}
)
```

## Respond to a Review

```python
review_id = "the-review-id"
response_data = {
    "data": {
        "type": "customerReviewResponses",
        "attributes": {
            "responseBody": "Thank you for your feedback. We've addressed this in our latest update."
        },
        "relationships": {
            "review": {
                "data": {"type": "customerReviews", "id": review_id}
            }
        }
    }
}
requests.post(
    "https://api.appstoreconnect.apple.com/v1/customerReviewResponses",
    headers=headers, json=response_data
)
```

**Note:** Each review can only have one developer response. Posting a new response replaces any existing one.

## Get Existing Response

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/customerReviews/{review_id}/response",
    headers=headers
)
RESPONSE_ID = response.json()['data']['id']
```

## Delete a Response

```python
# Use RESPONSE_ID from "Get Existing Response" above
requests.delete(
    f"https://api.appstoreconnect.apple.com/v1/customerReviewResponses/{RESPONSE_ID}",
    headers=headers
)
```

## AI-Assisted Review Summarization

Apple provides AI-generated review summaries:

```python
response = requests.get(
    f"https://api.appstoreconnect.apple.com/v1/apps/{APP_ID}/customerReviewSummarizations",
    headers=headers
)
```

## AI-Assisted Review Response Workflow

For responding to reviews using Claude:

1. Fetch all unresponded reviews (filter by low ratings first)
2. For each review, ask Claude to:
   - Translate the review if not in English
   - Identify the core issue or compliment
   - Generate a professional, empathetic response
   - Keep response under 5970 characters (API limit)
3. POST the response via the customerReviewResponses endpoint

Response guidelines:
- Professional and empathetic tone
- Acknowledge the specific issue mentioned
- Provide a concrete solution or timeline if possible
- Direct to support@yourcompany.com for complex issues
- Thank positive reviewers and mention upcoming features
