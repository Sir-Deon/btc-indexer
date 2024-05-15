from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Retrieve the payload from the incoming request
    payload = request.json
    # Notification can be sent to the user via email, sms or push notifications
    print(payload)
    
    return 'Notification received successfully'

if __name__ == '__main__':
    app.run()