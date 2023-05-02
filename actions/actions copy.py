# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
import sqlite3
import os
import traceback
import logging
from typing import Any, Text, Dict, List, Tuple, Optional
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
from typing import Dict, Union, List, Set

db_path_name = "/home/mark/chatbot/db/Molecules.db"
# db_virus_knowledgebase = '/home/mark/chatbot/db/Viruses.db'


global_pending: Set[str] = set([])
global_results: Dict[str, List[Dict[str, Union[int, str, float]]]] = {}

import threading
import time
import psycopg2

# Define a function that will run the database query
def run_query():
    #conn = psycopg2.connect(database="mydatabase", user="myusername", password="mypassword", host="localhost", port="5432")
    #cur = conn.cursor()
    #cur.execute("SELECT * FROM mytable")
    #rows = cur.fetchall()
    #for row in rows:
    #    print(row)
    #conn.close()
    time.sleep(5)




# _______________________________________________________________________________________________________________
# trigger this with 'sqltest' or 'testsql'
# !!Note this works without error
class TestSQL(Action):
    def name(self) -> Text:
        return "action_test_sql"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="running: action_test_sql")
        try:
            query = "SELECT * FROM MOLECULES LIMIT 1;"+str(time.time())
            print("starting run")
            #rows, errors = rows, errors = db_query(query, dispatcher)
            # Create a thread for the database query
            query_thread = threading.Thread(target=run_query)

            # Start the thread
            query_thread.start()

            # Poll the thread periodically from the main thread to check if it's still running
            while query_thread.is_alive():
                print("Query is running in the background...")
                time.sleep(1)

            # The database query has finished, so join the thread to the main thread
            query_thread.join()

            print("Done!")
            print("results:")
            #print(rows, errors)
            results = "results: \n"
            #for row in rows:
            #    results += f"{row}\n"
            #if errors != "":
            #    dispatcher.utter_message(text=errors)
            #dispatcher.utter_message(text=results)
        # except sqlite3.Error as e:
        # dispatcher.utter_message(text = e);
        except Exception as e1:
            dispatcher.utter_message(
                text="error while executing: " + traceback.format_exc()
            )

        return []


# __________________________________________________________________________________________________


# Count all molecules in MOLECULES table (unique set)____________________________________________________________
# trigger this with count molecules
# !!Note this one fails .. seems simple enough
class ActionSQLiteCountMolecules(Action):
    def name(self) -> Text:
        return "action_sqlite_count_unique_molecules"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # sql = 'SELECT COUNT(ID) AS Count FROM MOLECULES;';
        sql = "SELECT MAX(_ROWID_) FROM Molecules LIMIT 1;"
        dispatcher.utter_message(text=sql)

        try:
            conn = sqlite3.connect(db_path_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                count = row[0]
                message = "unique molecules: " + f"{count}"
                dispatcher.utter_message(text=message)

            conn.close()

        except Exception as e:
            # handle the error gracefully
            error_message = "I'm sorry, there was a problem processing your request."
            dispatcher.utter_message(text=error_message)

        return []

dispatcher: CollectingDispatcher = CollectingDispatcher()
ts = TestSQL()
ts.run(dispatcher, None, None)



