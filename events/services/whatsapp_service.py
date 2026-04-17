from twilio.rest import Client
from django.conf import settings
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_whatsapp_message(phone, message):

    try:
        client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',  # Twilio sandbox number
            # to=f'whatsapp:{phone}'
            to=f'whatsapp:+919958066256'
        )
        print("WhatsApp sent successfully")

    except Exception as e:
        print("WhatsApp Error:", str(e))