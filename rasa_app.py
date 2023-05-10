import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
rasa_endpoint = 'http://localhost:5005/webhooks/rest/webhook'  # replace with your Rasa endpoint

# Define the URL of the Rasa action server
rasa_action_endpoint = "http://localhost:5055/webhook"




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/messages', methods=['POST'])
def send_message():
    message = request.json['message']
    rasa_payload = {
        'sender': 'user',
        'message': message
    }
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()
    message_txt = ""
    for obj in rasa_response:
        message_txt += obj['text']
        message_txt += "\n<br>"
    response = {'message': message_txt}
    return jsonify(response)

@app.route('/api/query_status', methods=['GET'])
def query_status():    
    rasa_payload = {
        'sender': 'user',
        'message': "check pending"
    }
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()
    message_txt = ""
    for obj in rasa_response:
        print(obj)
        message_txt += obj['text']
        print(message_txt)
        message_txt += "\n<br>"
    response = {'message': message_txt}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

