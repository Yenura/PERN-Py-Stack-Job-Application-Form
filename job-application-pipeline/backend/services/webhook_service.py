import requests
from config import WEBHOOK_URL

def send_webhook(payload, candidate_email):
    """
    Send a webhook with the CV data to the provided endpoint
    """
    headers = {
        'Content-Type': 'application/json',
        'X-Candidate-Email': candidate_email
    }
    
    response = requests.post(
        WEBHOOK_URL,
        json=payload,
        headers=headers
    )
    
    # Check if request was successful
    response.raise_for_status()
    return response.json()