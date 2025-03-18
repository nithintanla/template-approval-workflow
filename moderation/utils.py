import openai
from django.conf import settings

# Keywords for content classification
REJECT_WORDS = ["smoke", "drink", "spa", "sex", "drugs"]
APPROVE_WORDS = ["discount", "offer", "sale", "deal"]

def moderate_campaign(content):
    """
    Uses an LLM to decide if a campaign template should be 'Approved', 'Rejected', or needs 'Manual' review.
    """
    # Check for direct keyword matches
    if any(word in content.lower() for word in REJECT_WORDS):
        return "Reject"
    if any(word in content.lower() for word in APPROVE_WORDS):
        return "Approve"
    
    # If uncertain, use LLM for deeper moderation
    prompt = f"""
    You are a content moderator for a marketing campaign. Classify the following message into:
    - "Reject" if it contains harmful or inappropriate words (e.g., smoking, drugs, adult content).
    - "Approve" if it contains promotional words (e.g., discount, offer).
    - "Manual" if it needs human review.

    Campaign Content:
    "{content}"

    Output one word: "Approve", "Reject", or "Manual".
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are a strict content moderator."},
                      {"role": "user", "content": prompt}],
            max_tokens=5,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return "Manual"  # Default to manual if LLM fails
