import logging
from io import StringIO
from typing import Any, Dict, List, Optional, Set, Text, Tuple

import pandas as pd
import requests
from flask import Flask, Response, jsonify, render_template, request, send_file

from constants import (action_tag, csv_str, csv_tag, histogram_tag,
                       intent_to_action, keyword_replacements, query_tag,
                       scatter_tag, svg_str, svg_tag)
from query import (async_run_query, check_pending, create_histogram_from_query,
                   create_scatter_from_query)

app = Flask(__name__)
rasa_endpoint = (
    "http://localhost:5005/webhooks/rest/webhook"  # replace with your Rasa endpoint
)

chembl_path = "./databases/chembl_33.db"


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
    orig_message = request.json["message"]    
    rasa_words = orig_message.split()
    cleaned_message = []
    for word in rasa_words:
        print(f"word: {word}")
        if word.upper() in keyword_replacements.keys():
            print(f"keyword found: {word}. not adding to new message")            
        else:
            cleaned_message.append(word)
    cleaned_str = " ".join(cleaned_message)
    print(f"rasa_message: {cleaned_str}")
    rasa_payload = {"sender": "user", "message": cleaned_str}
    rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()

    for obj in rasa_response:
        rasa_text = obj.get("text")
        print(f"text: {rasa_text}")
        element_list = obj.get("elements")
        print(f"elements: {element_list}")
        json_data = obj.get("json_message")
        print(f"json: {json_data}")
        print()
        if rasa_text:
            return create_response(rasa_text, orig_message)


def create_response(rasa_text, orig_message) -> Response:
    message_txt = ""
    queries = []
    
    print("creating response")
    print(orig_message)
    print(rasa_text)
    
    action_text = intent_to_action.get(rasa_text.upper())
    if not action_text:
        return jsonify({"message": rasa_text})
    
    print(f"determining action from text: {action_text}")
    if query_tag in action_text:
        query_text = action_text.replace(query_tag, "")
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
    if histogram_tag in action_text:
        query_text = action_text.replace(histogram_tag, "")
        keyword = find_keyword(orig_message, keyword_replacements)
        query_text = query_text.replace("$TOKEN$", keyword)
        queries.append(query_text)
        print(f"running histogram query \n{query_text}\n")
        hist_svg = create_histogram_from_query(query_text, keyword)
        return jsonify({"message": message_txt, "svg": hist_svg})
    if scatter_tag in action_text:
        query_text = action_text.replace(scatter_tag, "")
        keywords = find_keywords(orig_message, keyword_replacements)
        xlabel = keywords[0]
        ylabel = keywords[1]
        query_text = query_text.replace("$TOKEN$", xlabel, 1)
        query_text = query_text.replace("$TOKEN$", ylabel, 1)
        print(query_text)
        queries.append(query_text)
        print(f"running scatter query \n{query_text}\n")
        hist_svg = create_scatter_from_query(query_text, xlabel, ylabel)
        return jsonify({"message": message_txt, "svg": hist_svg})
    if action_tag in action_text:
        load_text = action_text.replace(action_tag, "")
        if svg_tag in load_text:
            return jsonify({"message": message_txt, "svg": svg_str})
        elif csv_tag in load_text:
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
