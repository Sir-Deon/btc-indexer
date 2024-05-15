import os
import requests # type: ignore
from retrying import retry # type: ignore
from flask import Flask, request # type: ignore

app = Flask(__name__)

def send_notification(payload):
    # This function can be modified to send notifications via email, SMS, push notifications, etc.
    print("Sending notification:", payload)

@retry(stop_max_attempt_number=3, wait_fixed=2000)  # Retry 3 times with a fixed 2-second delay between retries
def send_webhook(payload, url):
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print("Webhook sent successfully!")

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Retrieve the payload from the incoming request
    payload = request.json
    
    # Send the webhook request with retry functionality
    try:
        send_webhook(payload, "https://example.com/webhook")
    except requests.exceptions.RequestException as err:
        print(f"Webhook failed: {err}")
        # Handle the failure or return an error response if needed
    
    # Send the notification
    send_notification(payload)
    
    return 'Notification received successfully'

if __name__ == '__main__':
    app.run()