import os
from twilio.rest import Client

def send_message(message, api_token, from_number, to_number):
    try:
        client = Client(api_token, os.getenv('TWILIO_AUTH_TOKEN'))

        message = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )

        print(f"WhatsApp message sent: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# Initialize Twilio auth token from environment variable or ini file if needed
os.environ['TWILIO_AUTH_TOKEN'] = os.getenv('TWILIO_AUTH_TOKEN', None)
