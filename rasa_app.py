import logging
from io import StringIO
from typing import Any, Dict, List, Optional, Set, Text, Tuple
import os
import pandas as pd
import requests
from flask import Flask, Response, jsonify, render_template, request, send_file

from constants import (action_tag, csv_str, csv_tag, histogram_tag,
                       intent_to_action, keyword_replacements, query_tag,
                       scatter_tag, svg_str, svg_tag, scaff_tag, mols_tag)
from query import (async_run_query, check_pending, create_histogram_from_query,
                   create_scatter_from_query)
import traceback

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
        rasa_response_text = obj.get("text")
        print(f"rasa response text: {rasa_response_text}")        
        if rasa_response_text:
            return create_response(rasa_response_text, orig_message)


def create_response(rasa_text, orig_message) -> Response:
    message_txt = ""
    queries = []
    
    print("creating response")
    print(orig_message)
    print(rasa_text)
    
    action_text = intent_to_action.get(rasa_text.upper())
    print("ACTION",action_text)
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
    if svg_tag in action_text:
        return jsonify({"message": message_txt, "svg": svg_str})
    if csv_tag in action_text:
        csv_data = StringIO(csv_str)
        df = pd.read_csv(csv_data, sep=",")
        csv_json = df.to_json(orient="records")
        return jsonify({"message": message_txt, "csv": csv_json})
    if scaff_tag in action_text:
        print("Choosing file..")
        return jsonify({"message": message_txt, "scaffold": True})
    if mols_tag in action_text:
        print("Choosing file..")
        return jsonify({"message": message_txt, "molecule": True})
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

@app.route("/api/scaffold", methods=["POST"])
def save_scaffold():
    print(request.files)    
    message_txt = None
    status = False

    try:
        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        # Define the path where you want to save the file
        save_directory = "scaffolds/files"

        # Create the directory if it doesn't exist
        os.makedirs(save_directory, exist_ok=True)

        # Construct the full path to save the file
        save_path = os.path.join(save_directory, file.filename)

        file.save(save_path)
        message_txt = "completed and pending queries"
        status = True
    except Exception as e:    
        message_txt = f"Error while processing scaffold file: {traceback.format_exc()}"        

    response = {
        "message": message_txt,
        "completed": status,
    }
    return jsonify(response)

@app.route("/api/molecule", methods=["POST"])
def save_molecule():
    print(request.files)

    file = request.files["file"]
    
    if file.filename == "":
        return "No selected file"
    
    # Define the path where you want to save the file
    save_directory = "molecules/files"
    
    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)
    
    # Construct the full path to save the file
    save_path = os.path.join(save_directory, file.filename)
    
    file.save(save_path)

    pending_queries, finished_queries = check_pending()
    message_txt = "completed and pending queries"

    response = {
        "message": message_txt,
        "completed": finished_queries, #status, error
    }
    return jsonify(response)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
