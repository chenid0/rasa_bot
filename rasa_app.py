import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
rasa_endpoint = 'http://localhost:5005/webhooks/rest/webhook'  # replace with your Rasa endpoint

@app.route('/api/messages', methods=['POST'])
def send_message():
    message = request.json['message']
    rasa_payload = {
        'sender': 'user',
        'message': message
    }
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()
    response = {'message': rasa_response[0]['text']}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

