import requests
from config import ACCESS_TOKEN, PHONE_NUMBER_ID

# normal message
def send_message(to, text):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    requests.post(url, headers=headers, json=data)


# approval buttons
def send_approval(to, project_id, customer, message):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": f"NEW ORDER\n\nCustomer: {customer}\nProject: {project_id}\n\n{message}"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"approve_{project_id}",
                            "title": "APPROVE"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": f"reject_{project_id}",
                            "title": "REJECT"
                        }
                    }
                ]
            }
        }
    }

    requests.post(url, headers=headers, json=data)