import requests
from flask import Flask, request, jsonify, render_template

import sqlite3
import os
import traceback
import logging
from typing import Any, Text, Dict, List, Tuple, Optional, Set
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import time
import os
import time
import sqlite3
from flask import Flask, jsonify
from multiprocessing import Process, Queue
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from functools import lru_cache
from typing import Dict, Union, List
import threading

svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"305\" height=\"352\">\
<g id=\"unmapped\">\
<g id=\"lines\" style=\"stroke:rgb(138,0,0);stroke-width:2\">\
 <line x1=\"265\" y1=\"350\" x2=\"276\" y2=\"330\" />\
 <line x1=\"276\" y1=\"330\" x2=\"266\" y2=\"313\" />\
 <line x1=\"266\" y1=\"298\" x2=\"276\" y2=\"280\" />\
 <line x1=\"276\" y1=\"283\" x2=\"290\" y2=\"283\" />\
 <line x1=\"276\" y1=\"278\" x2=\"290\" y2=\"278\" />\
 <line x1=\"276\" y1=\"280\" x2=\"265\" y2=\"263\" />\
 <line x1=\"253\" y1=\"256\" x2=\"233\" y2=\"256\" />\
 <line x1=\"265\" y1=\"248\" x2=\"275\" y2=\"231\" />\
 <line x1=\"233\" y1=\"256\" x2=\"218\" y2=\"231\" />\
 <line x1=\"218\" y1=\"231\" x2=\"228\" y2=\"213\" />\
 <line x1=\"240\" y1=\"206\" x2=\"261\" y2=\"206\" />\
 <line x1=\"228\" y1=\"199\" x2=\"217\" y2=\"181\" />\
 <line x1=\"261\" y1=\"206\" x2=\"275\" y2=\"231\" />\
 <line x1=\"220\" y1=\"183\" x2=\"227\" y2=\"170\" />\
 <line x1=\"215\" y1=\"180\" x2=\"222\" y2=\"168\" />\
 <line x1=\"217\" y1=\"181\" x2=\"189\" y2=\"182\" />\
 <line x1=\"189\" y1=\"182\" x2=\"175\" y2=\"207\" />\
 <line x1=\"189\" y1=\"182\" x2=\"178\" y2=\"164\" />\
 <line x1=\"175\" y1=\"207\" x2=\"146\" y2=\"207\" />\
 <line x1=\"146\" y1=\"207\" x2=\"132\" y2=\"232\" />\
 <line x1=\"130\" y1=\"233\" x2=\"137\" y2=\"246\" />\
 <line x1=\"134\" y1=\"231\" x2=\"141\" y2=\"243\" />\
 <line x1=\"132\" y1=\"232\" x2=\"117\" y2=\"232\" />\
 <line x1=\"166\" y1=\"157\" x2=\"145\" y2=\"157\" />\
 <line x1=\"143\" y1=\"156\" x2=\"136\" y2=\"169\" />\
 <line x1=\"148\" y1=\"158\" x2=\"141\" y2=\"171\" />\
 <line x1=\"145\" y1=\"157\" x2=\"131\" y2=\"132\" />\
 <line x1=\"131\" y1=\"132\" x2=\"145\" y2=\"108\" />\
 <line x1=\"128\" y1=\"128\" x2=\"140\" y2=\"107\" />\
 <line x1=\"131\" y1=\"132\" x2=\"111\" y2=\"133\" />\
 <line x1=\"145\" y1=\"108\" x2=\"130\" y2=\"83\" />\
 <line x1=\"130\" y1=\"83\" x2=\"102\" y2=\"83\" />\
 <line x1=\"128\" y1=\"88\" x2=\"104\" y2=\"88\" />\
 <line x1=\"130\" y1=\"83\" x2=\"140\" y2=\"65\" />\
 <line x1=\"102\" y1=\"83\" x2=\"88\" y2=\"108\" />\
 <line x1=\"88\" y1=\"108\" x2=\"98\" y2=\"126\" />\
 <line x1=\"93\" y1=\"107\" x2=\"101\" y2=\"122\" />\
 <line x1=\"88\" y1=\"108\" x2=\"59\" y2=\"108\" />\
 <line x1=\"59\" y1=\"108\" x2=\"45\" y2=\"133\" />\
 <line x1=\"54\" y1=\"108\" x2=\"41\" y2=\"129\" />\
 <line x1=\"59\" y1=\"108\" x2=\"44\" y2=\"84\" />\
 <line x1=\"45\" y1=\"133\" x2=\"16\" y2=\"134\" />\
 <line x1=\"16\" y1=\"134\" x2=\"2\" y2=\"109\" />\
 <line x1=\"19\" y1=\"129\" x2=\"7\" y2=\"108\" />\
 <line x1=\"2\" y1=\"109\" x2=\"16\" y2=\"84\" />\
 <line x1=\"16\" y1=\"84\" x2=\"44\" y2=\"84\" />\
 <line x1=\"18\" y1=\"89\" x2=\"42\" y2=\"89\" />\
 <line x1=\"153\" y1=\"58\" x2=\"173\" y2=\"58\" />\
 <line x1=\"140\" y1=\"51\" x2=\"130\" y2=\"33\" />\
 <line x1=\"173\" y1=\"58\" x2=\"187\" y2=\"33\" />\
 <line x1=\"187\" y1=\"33\" x2=\"177\" y2=\"15\" />\
 <line x1=\"164\" y1=\"8\" x2=\"144\" y2=\"8\" />\
 <line x1=\"144\" y1=\"8\" x2=\"130\" y2=\"33\" />\
</g>\
<g id=\"letters\" fill=\"rgb(138,0,0)\" text-anchor=\"start\" font-family=\"Arial\" text-rendering=\"geometricPrecision\">\
<text x=\"256\" y=\"311\" font-size=\"14\">O</text>\
<text x=\"293\" y=\"286\" font-size=\"14\">O</text>\
<text x=\"255\" y=\"262\" font-size=\"14\">N</text>\
<text x=\"226\" y=\"212\" font-size=\"14\">N</text>\
<text x=\"223\" y=\"167\" font-size=\"14\">O</text>\
<text x=\"138\" y=\"258\" font-size=\"14\">O</text>\
<text x=\"103\" y=\"238\" font-size=\"14\">O</text>\
<text x=\"94\" y=\"238\" font-size=\"14\">H</text>\
<text x=\"168\" y=\"163\" font-size=\"14\">N</text>\
<text x=\"168\" y=\"150\" font-size=\"14\">H</text>\
<text x=\"128\" y=\"183\" font-size=\"14\">O</text>\
<text x=\"96\" y=\"139\" font-size=\"14\">N</text>\
<text x=\"139\" y=\"64\" font-size=\"14\">N</text>\
<text x=\"167\" y=\"14\" font-size=\"14\">O</text>\
</g>\
</g>\
<g id=\"mapped\">\
<g id=\"lines\" style=\"stroke:rgb(0,0,138);stroke-width:2\">\
</g>\
<g id=\"letters\" fill=\"rgb(0,0,138)\" text-anchor=\"start\" font-family=\"Arial\" text-rendering=\"geometricPrecision\">\
</g>\
</g>\
</svg>";

db_path_name = "/home/mark/chatbot/db/Molecules.db"
# db_virus_knowledgebase = '/home/mark/chatbot/db/Viruses.db'
thread_query_dict = dict()


global_results: Dict[str, List[Dict[str, Union[int, str, float]]]] = {}

# lock to ensure thread safety
lock = threading.Lock()


# function to add an item to the global dictionary
def add_pending_thread(key, value):
    global lock, thread_query_dict
    with lock:
        thread_query_dict[key] = value


# function to remove an item from the global dictionary
def remove_thread(key):
    global lock, thread_query_dict
    with lock:
        del thread_query_dict[key]


# function to retrieve an item from the global dictionary
def get_pending_query(key):
    global lock, thread_query_dict
    with lock:
        return thread_query_dict.get(key)


def get_all_pending_queries():
    global lock, thread_query_dict
    with lock:
        return thread_query_dict.items()


# function to add an item to the global dictionary
def add_query_result(key, value):
    global lock, global_results
    with lock:
        global_results[key] = value


# function to remove an item from the global dictionary
def remove_query(key):
    global lock, global_results
    with lock:
        del global_results[key]


# function to retrieve an item from the global dictionary
def get_query_result(key):
    global lock, global_results
    with lock:
        return global_results.get(key)


def get_all_query_results():
    global lock, global_results
    with lock:
        return global_results.items()


def run_query(query):
    try:
        conn = sqlite3.connect(db_path_name)
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        results = ""

        column_names = [description[0] for description in cur.description]
        # Print out the rows with column names
        for row in rows:
            for i in range(len(column_names)):
                results += str(column_names[i] + ": " + str(row[i]))
        conn.close()
        add_query_result(query, rows)
        time.sleep(15)
    except Exception as e:
        add_query_result(query, traceback.format_exc())


def async_run_query(query: str) -> None:
    try:
        query_thread = threading.Thread(target=run_query, args=(query,))
        # Start the thread
        query_thread.start()
        add_pending_thread(query_thread, query)

        # Poll the thread periodically from the main thread to check if it's still running
        start_time = time.time()
        while (time.time() - start_time) < 5 and query_thread.is_alive():
            print("Query is running in the background...")
            time.sleep(1)

        if query_thread.is_alive():
            print("query still running...exiting")

        if not query_thread.is_alive():
            # The database query has finished, so join the thread to the main thread
            query_thread.join()
            remove_thread(query_thread)
            results = "results: \n"
            results += str(get_query_result(query))
            print(results)
    except Exception as e:
        print(traceback.format_exc())


# _______________________________________________________________________________________________________________
# trigger this with 'check pending'
# !!Note this works without error
def check_pending() -> Tuple[Set[Text],Dict[Text, Any]]:                
        try:
            num_queries = get_all_pending_queries().__len__()
            
            print(f"{num_queries} queries already running")

            for thread, query in dict(get_all_pending_queries()).items():
                if thread.is_alive():
                    print(f"pending query: {query}")
                else:
                    remove_thread(thread)
                    print("thread finished. removing from set")

            for k, v in dict(get_all_query_results()).items():
                print(f"completed query: {k} : {v}")
                remove_query(k)
       
         

            return set(thread_query_dict.values()), dict(get_all_query_results())
        except Exception as e1:
            print("error while executing: " + traceback.format_exc())

        return set(), dict()


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
        if "query:" in obj["text"]:
            query_text = obj["text"].replace("query:", "").replace(" : ", "")
            async_run_query(query_text)
        message_txt += obj["text"]
        message_txt += "\n<br>"
    pending, completed = check_pending()
    if query_text in completed:
        response = {"message": str(completed[query_text])}
        return jsonify(response)
    return jsonify({"message": message_txt})


@app.route("/api/query_status", methods=["GET"])
def query_status():
    #rasa_payload = {"sender": "user", "message": "check pending"}
    #rasa_response = requests.post(rasa_endpoint, json=rasa_payload).json()
    #print("query status: rasa responded")
    #print(rasa_response)
    #print("end response")
    # [{'recipient_id': 'user', 'text': 'running: action_check_pending'}, {'recipient_id': 'user', 'text': '1 queries already running'}, {'recipient_id': 'user', 'text': 'thread finished. removing from set'}]

    pending_queries, finished_queries = check_pending()
    message_txt = ""
        
    response = {
        "message": "completed and pending queries",
        "pending": list(pending_queries),
        "completed": finished_queries,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
