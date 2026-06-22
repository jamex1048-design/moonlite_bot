from flask import Flask, request
import uuid
from datetime import datetime

from whatsapp import send_message, send_approval
from database import save_order
from config import VERIFY_TOKEN, FRIEND_NUMBER

app = Flask(__name__)

# -----------------------------
# SIMPLE MEMORY (USER STATE)
# -----------------------------
user_state = {}


# -----------------------------
# VERIFY WEBHOOK
# -----------------------------
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "invalid token"


# -----------------------------
# MAIN BOT
# -----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        text = msg['text']['body'].strip()
        user = msg['from']

        # save state if not exists
        if user not in user_state:
            user_state[user] = "HOME"


        # -----------------------------
        # HOME MENU
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
            return "ok"


        # -----------------------------
        # 1. WEBSITE MODULE
        # -----------------------------
        if text == "1":

            user_state[user] = "WEBSITE"

            send_message(user,
                "🌐 WEBSITE DEVELOPMENT\n\n"
                "Chagua aina ya website:\n\n"
                "1. Business Website\n"
                "2. Hotel / Lodge Website\n"
                "3. School Website\n"
                "4. Online Shop (E-commerce)\n"
                "5. Portfolio Website"
            )
            return "ok"


        # -----------------------------
        # WEBSITE TYPES
        # -----------------------------
        if user_state[user] == "WEBSITE":

            if text == "1":

                user_state[user] = "WEB_BUSINESS"

                send_message(user,
                    "👍 BUSINESS WEBSITE\n\n"
                    "Hii ni website ya biashara yako.\n\n"
                    "📌 Itakuwa na:\n"
                    "- Maelezo ya biashara\n"
                    "- WhatsApp button\n"
                    "- Google Maps\n"
                    "- Picha za huduma\n\n"
                    "👉 Tuma:\nJina la biashara yako + unachouza"
                )
                return "ok"


            if text == "2":

                user_state[user] = "WEB_HOTEL"

                send_message(user,
                    "🏨 HOTEL WEBSITE\n\n"
                    "📌 Inaonyesha:\n"
                    "- Vyumba\n"
                    "- Bei\n"
                    "- Booking system\n\n"
                    "👉 Tuma:\nJina la hotel + location + bei za vyumba"
                )
                return "ok"


            if text == "3":

                user_state[user] = "WEB_SCHOOL"

                send_message(user,
                    "🎓 SCHOOL WEBSITE\n\n"
                    "📌 Inaonyesha:\n"
                    "- Matokeo\n"
                    "- Matangazo\n"
                    "- Taarifa za shule\n\n"
                    "👉 Tuma:\nJina la shule + level (Primary/Secondary)"
                )
                return "ok"


            if text == "4":

                user_state[user] = "WEB_SHOP"

                send_message(user,
                    "🛒 E-COMMERCE WEBSITE\n\n"
                    "📌 Inaweza:\n"
                    "- Kuuza bidhaa\n"
                    "- Kupokea orders\n"
                    "- WhatsApp integration\n\n"
                    "👉 Tuma:\nUnauza nini?"
                )
                return "ok"


            if text == "5":

                user_state[user] = "WEB_PORTFOLIO"

                send_message(user,
                    "👤 PORTFOLIO WEBSITE\n\n"
                    "📌 Inaonyesha:\n"
                    "- Jina lako\n"
                    "- Skills\n"
                    "- Kazi zako\n\n"
                    "👉 Tuma:\nJina + kazi yako + skills"
                )
                return "ok"


        # -----------------------------
        # 2. GOOGLE MAPS
        # -----------------------------
        if text == "2":

            user_state[user] = "MAPS"

            send_message(user,
                "📍 GOOGLE MAPS BUSINESS\n\n"
                "Tuma:\n"
                "- Jina la biashara\n"
                "- Location\n"
                "- Namba ya simu"
            )
            return "ok"


        # -----------------------------
        # 3. BOOKING SYSTEM
        # -----------------------------
        if text == "3":

            user_state[user] = "BOOKING"

            send_message(user,
                "📅 BOOKING SYSTEM\n\n"
                "Tuma:\n"
                "- Jina\n"
                "- Namba\n"
                "- Huduma unayotaka"
            )
            return "ok"


        # -----------------------------
        # 4. PRICES
        # -----------------------------
        if text == "4":

            send_message(user,
                "💰 PRICE LIST\n\n"
                "Website:\n- Business: 150,000+\n- Hotel: 250,000+\n- Shop: 300,000+\n\n"
                "Google Maps: 30,000\n"
                "Booking System: 80,000+\n\n"
                "Deposit: 50% kabla ya kazi kuanza"
            )
            return "ok"


        # -----------------------------
        # 5. TRAINING
        # -----------------------------
        if text == "5":

            send_message(user,
                "🎓 MAFUNZO\n\n"
                "Tunafundisha:\n"
                "- HTML & CSS\n"
                "- JavaScript\n"
                "- Python\n"
                "- Website Development\n\n"
                "👉 Tuma ni course gani unataka"
            )
            return "ok"


        # -----------------------------
        # 6. TALK TO AGENT
        # -----------------------------
        if text == "6":

            send_message(user,
                "👨‍💼 Mtoa huduma atakuwasiliana nawe.\n\n"
                "Tuma:\n"
                "- Jina\n"
                "- Namba\n"
                "- Unachotaka"
            )
            return "ok"


        # -----------------------------
        # PAYMENT TRIGGER
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

            send_approval(
                FRIEND_NUMBER,
                project_id,
                user,
                text
            )

            return "ok"


        # -----------------------------
        # DEFAULT ORDER SAVE
        # -----------------------------
        project_id = "MT-" + str(uuid.uuid4())[:8]

        save_order(project_id, user, text, "NEW_ORDER")

        send_message(user,
            "✅ Tumepokea maombi yako.\n"
            f"Project ID: {project_id}\n"
            "Timu itakufuatilia."
        )

        send_approval(
            FRIEND_NUMBER,
            project_id,
            user,
            text
        )

        return "ok"


    except Exception as e:
        print("ERROR:", e)

    return "ok"


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)