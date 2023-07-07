import logging
from io import StringIO
import pandas as pd
import requests
from flask import Flask, jsonify, render_template, request, send_file, Response
from constants import (
    action_tag,
    csv_str,
    csv_tag,
    query_tag,
    svg_str,
    svg_tag,
    histogram_tag,
    scatter_tag,
    keyword_replacements, 
    keywords_for_spellcheck
)
from query import (
    async_run_query,
    check_pending,
    create_histogram_from_query,
    create_scatter_from_query,
)
from edit_distance import compare_to_string
from typing import Any, Dict, List, Optional, Set, Text, Tuple

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


def find_keywords(sentence: str, keywords: Dict[str, str]) -> List[str]:
    print(sentence)
    keywords_found = []
    words = sentence.split()
    for word in words:
        for keyword, replacement in keywords.items():
            if keyword.upper() in word.upper():
                print(f"keyword found: {keyword} -> {replacement}")
                keywords_found.append(replacement)
    if not keywords_found:
        print("no keyword found. defaulting to logP_rdkit")
        keywords_found.append("logP_rdkit")
        keywords_found.append("sarea_rdkit")
    return keywords_found


def find_keyword(sentence: str, keywords: Dict[str, str]) -> str:
    print(sentence)
    for keyword, replacement in keywords.items():
        if keyword.upper() in sentence.upper():
            print(f"keyword found: {keyword} -> {replacement}")
            return replacement
    print("no keyword found. defaulting to logP_rdkit")
    return "logP_rdkit"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/messages", methods=["POST"])
def send_message():
    orig_message = request.json.get("message")
    if not orig_message:
        return jsonify({"message": "No message provided"})

    rasa_words = orig_message.split()
    spell_checked = []
    for word in rasa_words:
        matches = compare_to_string(keywords_for_spellcheck, word, max_edit_distance=1)
        print(f"matches: {matches}")
        if len(matches) > 1:
            print(f"matches: {matches}")
        elif len(matches) == 1:
            spell_checked.append(next(iter(matches)))
        else:
            spell_checked.append(word)
            
    spell_checked_str = ' '.join(spell_checked)
    cleaned_message = replace_keywords(spell_checked_str)    
    print(f"rasa_message: {cleaned_message}")
    rasa_payload = {"sender": "user", "message": cleaned_message}
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()

    for obj in rasa_response:
        text = obj.get("text")
        print(f"text: {text}")
        element_list = obj.get("elements")
        print(f"elements: {element_list}")
        json_data = obj.get("json_message")
        print(f"json: {json_data}")
        print()
        if text:
            return create_response(text, orig_message)

def replace_keywords(message: str) -> str:
    cleaned_str = message
    for keyword_phrase in keyword_replacements.keys():
        keyword_phrase_upper = keyword_phrase.upper()
        cleaned_str = message.replace(' ' + keyword_phrase_upper + ' ', ' ')
        cleaned_str = message.replace(' ' + keyword_phrase_upper, '')  # Check if phrase is at the end    
    return cleaned_str


def create_response(text, message) -> Response:
    message_txt = ""
    queries = []
    print(f"determining action from text: {text}")
    if query_tag in text:
        query_text = text.replace(query_tag, "")
        queries.append(query_text)
        print(f"running async query \n{query_text}\n")
        async_run_query(query_text)
        pending, completed = check_pending()
        for query in queries:
            if query in pending:
                message_txt += f"query: {query} is pending\n<br>"
            if query in completed:
                message_txt += (
                    f"query: {query} is completed\n<br>{completed.get(query)}\n<br>"
                )
        return jsonify({"message": message_txt})
    if histogram_tag in text:
        query_text = text.replace(histogram_tag, "")
        keyword = find_keyword(message, keyword_replacements)
        query_text = query_text.replace("$TOKEN$", keyword)
        queries.append(query_text)
        print(f"running histogram query \n{query_text}\n")
        hist_svg = create_histogram_from_query(query_text, keyword)
        return jsonify({"message": message_txt, "svg": hist_svg})
    if scatter_tag in text:
        query_text = text.replace(scatter_tag, "")
        keywords = find_keywords(message, keyword_replacements)
        xlabel = keywords[0]
        ylabel = keywords[1]
        query_text = query_text.replace("$TOKEN$", xlabel, 1)
        query_text = query_text.replace("$TOKEN$", ylabel, 1)
        print(query_text)
        queries.append(query_text)
        print(f"running scatter query \n{query_text}\n")
        hist_svg = create_scatter_from_query(query_text, xlabel, ylabel)
        return jsonify({"message": message_txt, "svg": hist_svg})
    if action_tag in text:
        action_text = text.replace(action_tag, "")
        if svg_tag in action_text:
            return jsonify({"message": message_txt, "svg": svg_str})
        elif csv_tag in action_text:
            csv_data = StringIO(csv_str)
            df = pd.read_csv(csv_data, sep=",")
            csv_json = df.to_json(orient="records")
            return jsonify({"message": message_txt, "csv": csv_json})
    return jsonify({"message": "no action taken"})


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
