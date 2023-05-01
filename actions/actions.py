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

db_path_name = "/home/mark/chatbot/db/Molecules.db"
# db_virus_knowledgebase = '/home/mark/chatbot/db/Viruses.db'


global_results: Dict[str, List[Dict[str, Union[int, str, float]]]] = {}


@lru_cache(maxsize=128)
def run_query(query: str, timeout: int):        
    p = Process(target=execute_query, args=(query,))
    p.start()        

def execute_query(query: str) -> None:
    conn = sqlite3.connect(db_path_name)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if query not in global_results:
        global_results[query] = None
    cur.execute(query)
    rows = [dict(row) for row in cur.fetchall()]
    cur.close()
    conn.close()
    global_results[query] = rows


def db_query(query: str, dispatcher: CollectingDispatcher) -> Tuple[list, str]:
    timeout_secs = 5
    run_query(query, timeout=timeout_secs)
    start_time = time.time()
    while(time.time() - start_time < timeout_secs):
        if query in global_results:
            result = global_results[query]
            if result:
                return result, ""
            else:
                dispatcher.utter_message(text="query found but not completed yet. Query still running")
        time.sleep(1)
    return [], f"query not completed yet. {len(global_results.keys())} Queries still running"




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
            rows, errors = rows, errors = db_query(query, dispatcher)
            results = "results: \n"
            for row in rows:
                results += f"{row}\n"
            if errors != "":
                dispatcher.utter_message(text=errors)
            dispatcher.utter_message(text=results)
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
