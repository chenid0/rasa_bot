import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
rasa_endpoint = (
    "http://localhost:5005/webhooks/rest/webhook"  # replace with your Rasa endpoint
)

# Define the URL of the Rasa action server
rasa_action_endpoint = "http://localhost:5055/webhook"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/messages", methods=["POST"])
def send_message():
    message = request.json["message"]
    rasa_payload = {"sender": "user", "message": message}
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()
    message_txt = ""
    for obj in rasa_response:
        message_txt += obj["text"]
        message_txt += "\n<br>"
    response = {"message": message_txt}
    return jsonify(response)


@app.route("/api/query_status", methods=["GET"])
def query_status():
    rasa_payload = {"sender": "user", "message": "check pending"}
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()
    print("query status: rasa responded")
    print(rasa_response)
    print("end response")
    #[{'recipient_id': 'user', 'text': 'running: action_check_pending'}, {'recipient_id': 'user', 'text': '1 queries already running'}, {'recipient_id': 'user', 'text': 'thread finished. removing from set'}]
        
    message_txt = ""
    pending_queries = []
    finished_queries = dict()
    for obj in rasa_response:
        print()
        print(obj)
        text = obj["text"]
        if "pending query" in text:
            text = text.replace("pending query:", "").strip()
            pending_queries.append(text)
        if "finished query" in text:
            text = text.replace("completed query:", "").strip()
            parts = text.split(":")
            finished_queries[parts[0]] = parts[1]            
        message_txt += text

        message_txt += "\n<br>"
    response = {"message": message_txt, "pending": pending_queries,"completed": finished_queries}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
