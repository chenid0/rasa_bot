import logging
from io import StringIO
import pandas as pd
import requests
from flask import Flask, jsonify, render_template, request, send_file
from constants import (
    action_tag,
    csv_str,
    csv_tag,
    query_tag,
    svg_str,
    svg_tag,
    histogram_tag,
)
from query import async_run_query, check_pending, create_histogram_from_query
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

# Get column names from "MOLPROPS" and "MOLDATA"
#  regex out (case insensitive compare) : could match multiple
#       'logp'-> 'logP_rdkit'
#       'HBA', 'Hydrogen Bond Acceptor', 'H-Bond Acceptor', HBond Acceptor', 'Acceptors'->'HBA'
#       'TPSA', 'PSA', 'Polar Surface'-> 'TPSA_rdkit'
#       'HBD', 'Hydrogen Bond Donar', 'HBond Donar', 'H-Bond Donar', 'Donar', 'Doner' -> 'HBD'
#       'Surface Area', 'SA' -> 'SArea_rdkit'
#       'fCSP3', 'fracCsp3','Fraction Csp3', 'number csp3 carbons' ->fracCSP3_rdkit
#       'Number of Spiroatoms', 'Number of spiro-atoms', 'spiroatoms', 'spiro-atoms', 'Spiro-atom-count' -> 'SpiroAtoms_rdkit'
#       'Number of BridgeHeadAtoms', Bridgehead count', 'bridgehead atoms' -> 'BridgeHeadAtoms_rdkit'
#       'RotBond', 'RotatableBond', 'Rotatable' -> 'Rotatable_bonds'
#       'MW','Molecular Weight', 'MolWeight', 'mass' -> 'MW'
#
#       ignore others for now

keyword_replacements = {
    "lopP": "logP_rdkit",
    "HBA": "HBA",
    "Hydrogen Bond Acceptor": "HBA",
    "H-Bond Acceptor": "HBA",
    "HBond Acceptor": "HBA",
    "Acceptors": "HBA",
    "TPSA": "TPSA_rdkit",
    "PSA": "TPSA_rdkit",
    "Polar Surface": "TPSA_rdkit",
    "HBD": "HBD",
    "Hydrogen Bond Donar": "HBD",
    "HBond Donar": "HBD",
    "H-Bond Donar": "HBD",
    "Donar": "HBD",
    "Doner": "HBD",
    "Surface Area": "SArea_rdkit",
    "SA": "SArea_rdkit",
    "fCSP3": "fracCSP3_rdkit",
    "fracCsp3": "fracCSP3_rdkit",
    "Fraction Csp3": "fracCSP3_rdkit",
    "number csp3 carbons": "fracCSP3_rdkit",
    "Number of Spiroatoms": "SpiroAtoms_rdkit",
    "Number of spiro-atoms": "SpiroAtoms_rdkit",
    "SpiroAtoms": "SpiroAtoms_rdkit",
    "spiroatoms": "SpiroAtoms_rdkit",
    "spiro-atoms": "SpiroAtoms_rdkit",
    "Spiro-atom-count": "SpiroAtoms_rdkit",
    "BridgeHeadAtoms": "BridgeHeadAtoms_rdkit",
    "Number of BridgeHeadAtoms": "BridgeHeadAtoms_rdkit",
    "Bridgehead count": "BridgeHeadAtoms_rdkit",
    "bridgehead atoms": "BridgeHeadAtoms_rdkit",
    "RotBond": "Rotatable_bonds",
    "RotatableBond": "Rotatable_bonds",
    "Rotatable": "Rotatable_bonds",
    "mass": "MW",
    "Molecular Weight": "MW",
    "MolWeight": "MW",
    "MW": "MW",
}


def find_keyword(sentence: str, keywords: Dict[str,str]) -> str:
    print(sentence)
    for keyword, replacement in keywords.items():
        print(keyword.capitalize(), " : " ,sentence.capitalize())
        if keyword.capitalize() in sentence.capitalize():
            print(f"keyword found: {keyword} -> {replacement}")
            return replacement
    print("no keyword found. defaulting to logP_rdkit")
    return "logP_rdkit"


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
                keyword = find_keyword(message, keyword_replacements)
                print(query_text)
                query_text = query_text.replace("$TOKEN$", keyword)
                print(query_text)
                queries.append(query_text)
                print(f"running histogram query \n{query_text}\n")
                hist_svg = create_histogram_from_query(query_text, keyword)          
                return jsonify({"message": message_txt, "svg": hist_svg})

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
            message_txt += (
                f"query: {query} is completed\n<br>{completed.get(query)}\n<br>"
            )
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
