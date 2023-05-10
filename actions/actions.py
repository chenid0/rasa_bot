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
from typing import Dict, Union, List
import threading

db_path_name = "/home/mark/chatbot/db/Molecules.db"
# db_virus_knowledgebase = '/home/mark/chatbot/db/Viruses.db'
thread_set = set()


global_results: Dict[str, List[Dict[str, Union[int, str, float]]]] = {}

# lock to ensure thread safety
lock = threading.Lock()

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

def async_run_query(query: str, dispatcher: CollectingDispatcher):
    try:
        query_thread = threading.Thread(target=run_query, args=(query,))
        # Start the thread
        query_thread.start()
        thread_set.add(query_thread)

        # Poll the thread periodically from the main thread to check if it's still running
        start_time = time.time()
        while (time.time() - start_time) < 5 and query_thread.is_alive():                
            print("Query is running in the background...")
            time.sleep(1)
        
        if query_thread.is_alive():
            dispatcher.utter_message(text="query still running...exiting")

        if not query_thread.is_alive():
            # The database query has finished, so join the thread to the main thread        
            query_thread.join()
            thread_set.remove(query_thread)
            results = "results: \n"
            results += str(get_query_result(query))
            dispatcher.utter_message(text=results)
    except Exception as e:
        dispatcher.utter_message(text=traceback.format_exc())


# _______________________________________________________________________________________________________________
# trigger this with 'check pending'
# !!Note this works without error
class CheckPending(Action):
    def name(self) -> Text:
            return "action_check_pending"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if not dispatcher:
            dispatcher = CollectingDispatcher()
        if not tracker:
            tracker = Tracker()
        dispatcher.utter_message(text="running: action_check_pending")
        try:
            num_queries = thread_set.__len__()
            if num_queries > 0:
                dispatcher.utter_message(text=f"{num_queries} queries already running")
            
            for thread in set(thread_set):
                if thread.is_alive():
                    dispatcher.utter_message(text="thread already running")                
                else:
                    thread_set.remove(thread)
                    dispatcher.utter_message(text="thread finished. removing from set")
            
            
            for k,v in dict(get_all_query_results()).items():
                if v:
                    dispatcher.utter_message(text=f"query results finished: {k} : {v}")
                    remove_query(k)
                else:
                    dispatcher.utter_message(text=f"query still pending: {k} ")
            return get_all_query_results()
        except Exception as e1:
            dispatcher.utter_message(
                text="error while executing: " + traceback.format_exc()
            )

        return []


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
            query = "SELECT * FROM MOLECULES LIMIT 1;"
            async_run_query(query, dispatcher)
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
        query = 'SELECT COUNT(ID) AS Count FROM MOLECULES;';
        #query = "SELECT MAX(_ROWID_) FROM Molecules LIMIT 1;"
        async_run_query(query, dispatcher)        
        return []


# _______________________________________________________________________________________________________________


# Count Moldata rows and group by library____________________________________________________________
class ActionSQLiteCountMolsByLibrary(Action):
    def name(self) -> Text:
        return "action_sqlite_count_molsbylibrary"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform: SELECT Library, COUNT(ID) AS Count FROM MOLDATA GROUP BY Library ORDER BY Library;"
        )
        return []

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT Library, COUNT(*) AS Count FROM MOLDATA GROUP BY Library ORDER BY Library;');
        # results = cursor.fetchall();

        # for row in results:
        #     name = row[0];
        #     count = row[1];
        #     message = f"{Library}: {count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Count all rows in MOLDATA____________________________________________________________
class ActionSQLiteCountVendorRows(Action):
    def name(self) -> Text:
        return "action_sqlite_count_vendor_rows"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform: SELECT COUNT(ID) AS Count FROM MOLDATA;"
        )
        return []

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT COUNT(ID) AS Count FROM MOLDATA;');
        # results = cursor.fetchall();

        # for row in results:
        #     count = row[0];
        #     message = "total: " + f"{count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Popup a javascript virus filter panel like in spotfire example_________________________________________________
class ActionPopupVirusFilter(Action):
    def name(self) -> Text:
        return "action_popup_virus_filter"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Popup a javascript virus filter panel like in spotfire example(actions.py)"
        )
        return []


# _______________________________________________________________________________________________________________


# Popup a javascript target filter panel like in spotfire example_______________________________________________
class ActionPopupTargetFilter(Action):
    def name(self) -> Text:
        return "action_popup_target_filter"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Popup a javascript target filter panel like in spotfire example(actions.py)"
        )
        return []


# _______________________________________________________________________________________________________________


# Popup a javascript Property Filter panel like in ChemVendor website___________________________________________
class ActionPopupPropertyFilter(Action):
    def name(self) -> Text:
        return "action_popup_property_filter"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Popup a javascript Property Filter panel like in ChemVendor website(actions.py)"
        )
        return []

        # formulate sql for MOLDATA table

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT * FROM TARGET_TABLE ;');
        # results = cursor.fetchall();

        # for row in results:
        #     name = row[0];
        #     count = row[1];
        #     message = "unique molecules: " + f"{count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Set Optoions to filter by vendor__________________________________________
class ActionPopupVendorFilter(Action):
    def name(self) -> Text:
        return "action_popup_vendor_filter"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform: SELECT COUNT(DISTINCT m.MOLID) as Count from MOLECULES m, MOLPROPS mp where m.MOLID == mp.MOLID AND mp.Library IN SET {VENDORS LIST};"
        )
        return []

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT COUNT(DISTINCT m.MOLID) as Count from MOLECULES m, MOLPROPS mp where m.MOLID == mp.MOLID AND mp.Library IN SET {VENDORS LIST};');
        # results = cursor.fetchall();

        # for row in results:
        #     count = row[0];
        #     message = "unique molecules: " + f"{count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Set Optons to filter PAINS molecules: return count ___________________________________________________________
class ActionFilterByPainsMotifs(Action):
    def name(self) -> Text:
        return "action_filter_by_pains"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform: SELECT COUNT(MOLID) as Count from MOLECULES m, MOLPROPS mp where m.MOLID == mp.MOLID AND mp.PAINS ISNULL;"
        )
        return []

        # note: i need to build this table yet

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT COUNT(MOLID) as Count from MOLECULES m, MOLPROPS mp where m.MOLID == mp.MOLID AND mp.PAINS ISNULL;');
        # results = cursor.fetchall();

        # for row in results:
        #     count = row[0];
        #     message = "unique molecules: " + f"{count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Set Optons to filter existing molecules: return count ___________________________________________________________
class ActionFilterByPainsMotifs2(Action):
    def name(self) -> Text:
        return "action_filter_by_pains"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform: SELECT COUNT(MOLID) as Count from MOLECULES m, MARKING mk where mk.MOLID == m.MOLID AND mk.PAINS ISNULL;"
        )
        return []

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT COUNT(MOLID) as Count from MOLECULES m, MARKING mk where mk.MOLID == m.MOLID AND mk.PAINS ISNULL');
        # results = cursor.fetchall();

        # for row in results:
        #     count = row[0];
        #     message = "unique molecules: " + f"{count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Set Optoions to filter by ugly molecules___________________________________________
class ActionFilterByUnstableMotifs(Action):
    def name(self) -> Text:
        return "action_filter_by_ugly_motifs"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform: SELECT COUNT(MOLID) as Count from MOLECULES m, MOLPROPS mp where m.MOLID == mp.MOLID AND mp.UGLY == FALSE;"
        )
        return []

        # conn = sqlite3.connect(db_path_name);
        # cursor = conn.cursor();

        # cursor.execute('SELECT COUNT(MOLID) as Count from MOLECULES m, MOLPROPS mp where m.MOLID == mp.MOLID AND mp.UGLY == FALSE;');
        # results = cursor.fetchall();

        # for row in results:
        #     count = row[0];
        #     message = "unique molecules: " + f"{count}";
        #     dispatcher.utter_message(text=message);

        # conn.close();

        # return [];


# _______________________________________________________________________________________________________________


# Set Optoions to filter by ugly molecules___________________________________________
class ActionPerformDiversityAnalysis(Action):
    def name(self) -> Text:
        return "action_perfrom_diversity_analysis"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Perform cluster analysis on the filtered set of molecules and add a numeric column (sequential) to the MOLPROPS;"
        )
        return []
