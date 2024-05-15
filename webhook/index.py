from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Retrieve the payload from the incoming request
    payload = request.json

    # Process the payload or perform actions based on the webhook data
    # Add your custom logic here
    print(payload)
    # Return a response (optional)
    return 'Webhook received successfully'

if __name__ == '__main__':
    app.run()