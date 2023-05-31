import sqlite3
import threading
import time
import traceback
from functools import lru_cache
from threading import Thread
from typing import Any, Dict, List, Set, Text, Tuple, Union
from constants import db_path_name

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
        #time.sleep(15)
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
        num_seconds_waiting = 5
        while (
            time.time() - start_time
        ) < num_seconds_waiting and query_thread.is_alive():
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


def check_pending() -> Tuple[Set[Text], Dict[Text, Any]]:
    try:
        num_queries = get_all_pending_queries().__len__()

        print(f"{num_queries} queries already running")

        for thread, query in dict(get_all_pending_queries()).items():
            if thread.is_alive():
                print(f"pending query: {query}")
            else:
                remove_thread(thread)
                print("thread finished. removing from set")

        completed_result = dict(get_all_query_results())
        for k, v in completed_result.items():
            print(f"completed query: {k} : {v}")
            remove_query(k)

        return set(thread_query_dict.values()), completed_result
    except Exception as e1:
        print("error while executing: " + traceback.format_exc())

    return set(), dict()