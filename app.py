from flask import Flask, request
import uuid
import requests
from datetime import datetime

from whatsapp import send_message, send_approval
from database import save_order
from config import VERIFY_TOKEN, FRIEND_NUMBER

app = Flask(__name__)

# -----------------------------
# WHATSAPP CLOUD API (NEW ADDITION ONLY)
# -----------------------------
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"


def cloud_send(to, message):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    requests.post(url, headers=headers, json=data)


def cloud_admin_alert(project_id, user, text):
    msg = f"""
🟡 CLOUD ALERT

Project: {project_id}
User: {user}
Request: {text}
"""

    cloud_send(FRIEND_NUMBER, msg)


# -----------------------------
# SIMPLE MEMORY (UNCHANGED)
# -----------------------------
user_state = {}


# -----------------------------
# VERIFY WEBHOOK (UNCHANGED)
# -----------------------------
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "invalid token"


# -----------------------------
# MAIN BOT (UNCHANGED LOGIC + ADD WHATSAPP CLOUD CALLS)
# -----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        text = msg['text']['body'].strip()
        user = msg['from']

        if user not in user_state:
            user_state[user] = "HOME"


        # -----------------------------
        # HOME MENU (UNCHANGED + ADD CLOUD)
        # -----------------------------
        if text.lower() in ["hi", "hello", "menu"]:

            user_state[user] = "HOME"

            send_message(user,
                "👋 KARIBU MOONLITE TECHNOLOGIES 🚀\n\n"
                "CHAGUA HUDUMA:\n\n"
                "1. Website Development\n"
                "2. Google Maps Business\n"
                "3. Booking System\n"
                "4. Price List\n"
                "5. Mafunzo (Training)\n"
                "6. Ongea na Mtoa Huduma\n"
            )

            # NEW ADDITION ONLY
            cloud_send(user, "👋 Welcome message (cloud backup active)")

            return "ok"


        # -----------------------------
        # WEBSITE MODULE (UNCHANGED)
        # -----------------------------
        if text == "1":

            user_state[user] = "WEBSITE"

            send_message(user,
                "🌐 WEBSITE DEVELOPMENT\n\n"
                "Chagua aina ya website:\n\n"
                "1. Business Website\n"
                "2. Hotel / Lodge Website\n"
                "3. School Website\n"
                "4. Online Shop\n"
                "5. Portfolio"
            )

            # NEW ADDITION ONLY
            cloud_send(user, "🌐 Website menu opened (cloud logged)")

            return "ok"


        # -----------------------------
        # PAYMENT TRIGGER (UNCHANGED + ADD CLOUD)
        # -----------------------------
        if "pay" in text.lower():

            project_id = "MT-" + str(uuid.uuid4())[:8]

            save_order(project_id, user, text, "PENDING_PAYMENT")

            send_message(user,
                "💰 MALIPO\n\n"
                "Deposit: 50%\n"
                "M-Pesa: 07XXXXXXXX\n\n"
                f"Project ID: {project_id}"
            )

            send_approval(FRIEND_NUMBER, project_id, user, text)

            # NEW ADDITIONS ONLY
            cloud_send(user, f"💰 Payment started for {project_id}")
            cloud_admin_alert(project_id, user, text)

            return "ok"


        # -----------------------------
        # DEFAULT ORDER (UNCHANGED + ADD CLOUD)
        # -----------------------------
        project_id = "MT-" + str(uuid.uuid4())[:8]

        save_order(project_id, user, text, "NEW_ORDER")

        send_message(user,
            "✅ Tumepokea maombi yako.\n"
            f"Project ID: {project_id}\n"
            "Timu itakufuatilia."
        )

        send_approval(FRIEND_NUMBER, project_id, user, text)

        # NEW ADDITIONS ONLY
        cloud_send(user, f"✅ Order received: {project_id}")
        cloud_admin_alert(project_id, user, text)

        return "ok"


    except Exception as e:
        print("ERROR:", e)

    return "ok"


# -----------------------------
# RUN SERVER (UNCHANGED)
# -----------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)