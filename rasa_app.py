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
    # Define the action to execute on the Rasa action server
    action = "action_check_pending"    

    # Define the data to send in the POST request
    data = {
        "next_action": action,
        "sender": "flask_app",
    }

    # Send a POST request to the Rasa action server
    response = requests.post(rasa_action_endpoint, json=data).json()

    # Print the response from the Rasa action server
    print(response)
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

