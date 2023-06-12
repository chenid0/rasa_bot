import logging
from io import StringIO
import pandas as pd
import requests
from flask import Flask, jsonify, render_template, request, send_file

from constants import (action_tag, csv_str, csv_tag, query_tag,
                       svg_str, svg_tag, histogram_tag)
from query import async_run_query, check_pending, run_histogram_query

"""
text: Optional[Text] = None,
image: Optional[Text] = None,
json_message: Optional[Dict[Text, Any]] = None,
template: Optional[Text] = None,
response: Optional[Text] = None,
attachment: Optional[Text] = None,
buttons: Optional[List[Dict[Text, Any]]] = None,
elements: Optional[List[Dict[Text, Any]]] = None,
"""


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
    queries = []
    for obj in rasa_response:
        text = obj.get("text")
        print(f"text: {text}")
        element_list = obj.get("elements")
        print(f"elements: {element_list}")
        json_data = obj.get("json_message")
        print(f"json: {json_data}")
        print()
        if text:
            if query_tag in text:
                query_text = obj["text"].replace(query_tag, "")
                queries.append(query_text)
                print(f"running async query \n{query_text}\n")
                async_run_query(query_text)
            if histogram_tag in text:
                query_text = obj["text"].replace(histogram_tag, "")
                queries.append(query_text)
                print(f"running histogram query \n{query_text}\n")
                bytes = run_histogram_query(query_text)
                return send_file(bytes, mimetype='image/png')

            if action_tag in text:            
                action_text = obj["text"].replace(action_tag, "")
                if svg_tag in action_text:
                    return jsonify({"message": message_txt, "svg": svg_str})
                elif csv_tag in action_text:
                    csv_data = StringIO(csv_str)
                    df = pd.read_csv(csv_data, sep=",")                
                    csv_json = df.to_json(orient="records")
                    return jsonify({"message": message_txt, "csv": csv_json})        
    pending, completed = check_pending()
    for query in queries:
        if query in pending:
            message_txt += f"query: {query} is pending\n<br>"
        if query in completed:
            message_txt += f"query: {query} is completed\n<br>{completed.get(query)}\n<br>"
    return jsonify({"message": message_txt})


@app.route("/api/query_status", methods=["GET"])
def query_status():
    pending_queries, finished_queries = check_pending()
    message_txt = "completed and pending queries"

    response = {
        "message": message_txt,
        "pending": list(pending_queries),
        "completed": finished_queries,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
