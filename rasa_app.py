import logging
from io import StringIO
import pandas as pd
import requests
import sqlite3
import csv 
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
)
from query import (
    async_run_query,
    check_pending,
    create_histogram_from_query,
    create_scatter_from_query,
)
from typing import Any, Dict, List, Optional, Set, Text, Tuple
from parse_yaml import parse_yaml_from_file


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
        text = obj.get("text")
        print(f"text: {text}")
        element_list = obj.get("elements")
        print(f"elements: {element_list}")
        json_data = obj.get("json_message")
        print(f"json: {json_data}")
        print()
        if text:
            return create_response(text, orig_message)


def create_response(orig_text, message) -> Response:
    message_txt = ""
    queries = []
    reponses_dict = parse_yaml_from_file("domain.yml")
    text = reponses_dict.get(orig_text)
    if not text:
        text = orig_text
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


def get_assay_id(assay_id):
    conn = sqlite3.connect("chembl_33.db")
    cursor = conn.cursor()
    if not assay_id.isnumeric():
        print("Please enter an integer")
    else:
        res = query(assay_id, cursor)
        gen_csv(res)
        print_results(res)
    cursor.close()
    conn.close()

def query(n, cursor) -> List[Tuple[str, int, int, str, float, str, str, int]]:
    query = f"""
    SELECT cs.canonical_smiles, act.activity_id, act.assay_id, act.standard_relation,
        act.standard_value, act.standard_units, act.standard_type, act.molregno
    FROM Activities AS act
    JOIN compound_structures AS cs ON act.molregno = cs.molregno
    WHERE act.assay_id = {n}
    LIMIT 1;
    """
    # Made query and received assay id, execute query
    cursor.execute(query)
    r = cursor.fetchall()
    return r
def gen_csv(results):
    output_file = "output.csv"
    # Generate and fill up CSV file with recently pulled data
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Canonical Smiles', 'Activity ID', 'Assay ID', 'Standard Relation',
                        'Standard Value', 'Standard Units', 'Standard Type', 'Molregno'])
        writer.writerows(results)

def print_results(results):
    # Print the results in command prompt
    for row in results:
        canonical_smiles, activity_id, assay_id, standard_relation, \
        standard_value, standard_units, standard_type, molregno = row
        
        print("Canonical Smiles:", canonical_smiles)
        print("Activity ID:", activity_id)
        print("Assay ID:", assay_id)
        print("Standard Relation:", standard_relation)
        print("Standard Value:", standard_value)
        print("Standard Units:", standard_units)
        print("Standard Type:", standard_type)
        print("Molregno:", molregno)

def get_virus(organism):    
    conn = sqlite3.connect(chembl_path)
    cursor = conn.cursor()
    query = f"""SELECT td.organism, td.pref_name, td.target_type FROM target_dictionary td WHERE td.organism like '%{organism}%' ORDER by td.organism"""
    # Made query and received assay id, execute query
    cursor.execute(query)
    r = cursor.fetchall()
    print(r)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
