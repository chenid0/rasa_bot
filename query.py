import csv
import sqlite3
import threading
import time
import traceback
from functools import lru_cache
from io import BytesIO, StringIO
from threading import Thread
from typing import Any, Dict, List, Set, Text, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np

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

        add_query_result(query, rows)
        # time.sleep(15)
    except Exception as e:
        print(f"error running query {query}")
        print(traceback.format_exc())
        add_query_result(query, traceback.format_exc())
    finally:
        conn.close()


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


def create_scatter_from_query(query: str, xlabel: str, ylabel: str) -> str:
    print(f"running scatter query {query}")
    run_query(query)
    data = get_query_result(query)
    print(f"results count = {len(data)}")
    remove_query(query)

    # Splitting the tuples into two lists
    x_data, y_data = zip(*data)

    # Convert the data to numpy arrays
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Creating the scatter plot
    plt.scatter(x_data, y_data)

    # Calculating the coefficients of the best-fit line
    slope, intercept = np.polyfit(x_data, y_data, 1)

    # Calculating the predicted y values
    y_pred = slope * x_data + intercept

    # Adding the best-fit line
    plt.plot(x_data, y_pred, color="red", label="Best-fit Line")

    # Calculate the R and R2 coefficient
    # Calculate the Pearson correlation coefficient
    r = np.corrcoef(x_data, y_data)[0, 1]
    r_squared = r**2

    # plt.text(0.05, 0.95, f'R2 = {r_squared:.2f}', transform=plt.gca().transAxes, ha='left', va='top')
    # Annotating the R-squared and Pearson coefficient
    plt.text(
        0.05,
        0.95,
        f"R2 = {r_squared:.2f}\nPearson = {r:.2f}",
        transform=plt.gca().transAxes,
        ha="left",
        va="top",
    )

    # Optionally, adding a title and labels
    plt.title("Scatter plot")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Save the image to a BytesIO object
    image_stream = StringIO()
    plt.savefig(image_stream, format="svg")
    plt.close()

    return image_stream.getvalue()


def create_histogram_from_query(
    query: str, xlabel: str, bins=10, min_threshold=0.01
) -> str:
    print(f"running histogram query {query}")
    run_query(query)
    data = get_query_result(query)
    remove_query(query)

    # Plotting the histogram
    field_values, counts = zip(*data)
    max_index = counts.index(max(counts))
    max_count = counts[max_index]
    max_field = field_values[max_index]
    threshold = min_threshold * max_count
    # filter out values that are less than the threshold
    filtered_fields = [
        field for field, count in zip(field_values, counts) if count >= threshold
    ]
    filtered_counts = [count for count in counts if count >= threshold]

    plt.bar(filtered_fields, filtered_counts, width=0.5)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel("Frequency")
    plt.title("Histogram")
    # Format y-axis tick labels
    plt.ticklabel_format(style="plain", axis="y")

    # Save the image to a BytesIO object
    image_stream = StringIO()
    plt.savefig(image_stream, format="svg")
    plt.close()

    return image_stream.getvalue()


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


def get_virus(organism):
    conn = sqlite3.connect(chembl_path)
    cursor = conn.cursor()
    query = f"""SELECT td.organism, td.pref_name, td.target_type FROM target_dictionary td WHERE td.organism like '%{organism}%' ORDER by td.organism"""
    # Made query and received assay id, execute query
    cursor.execute(query)
    r = cursor.fetchall()
    print(r)


def query(assay_id, cursor) -> List[Tuple[str, int, int, str, float, str, str, int]]:
    query = f"""
    SELECT cs.canonical_smiles, act.activity_id, act.assay_id, act.standard_relation,
        act.standard_value, act.standard_units, act.standard_type, act.molregno
    FROM Activities AS act
    JOIN compound_structures AS cs ON act.molregno = cs.molregno
    WHERE act.assay_id = {assay_id};
    """
    # Made query and received assay id, execute query
    cursor.execute(query)
    r = cursor.fetchall()
    return r


def print_results(results):
    # Print the results in command prompt
    for row in results:
        (
            canonical_smiles,
            activity_id,
            assay_id,
            standard_relation,
            standard_value,
            standard_units,
            standard_type,
            molregno,
        ) = row

        print("Canonical Smiles:", canonical_smiles)
        print("Activity ID:", activity_id)
        print("Assay ID:", assay_id)
        print("Standard Relation:", standard_relation)
        print("Standard Value:", standard_value)
        print("Standard Units:", standard_units)
        print("Standard Type:", standard_type)
        print("Molregno:", molregno)


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


def gen_csv(results):
    output_file = "output.csv"
    # Generate and fill up CSV file with recently pulled data
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "Canonical Smiles",
                "Activity ID",
                "Assay ID",
                "Standard Relation",
                "Standard Value",
                "Standard Units",
                "Standard Type",
                "Molregno",
            ]
        )
        writer.writerows(results)
