from collections import namedtuple
import csv
import os

from minet import multithreaded_fetch
from configure_data import TestData

OUTPUT_UNRESPONSIVE_URLS_PATHFILE = os.path.join("data", "unresponsiveURL.csv")
PRIVATE_OUTPUT_FETCHED_URLS_PATHFILE = os.path.join("data", "private.ural_results.csv")
PUBLIC_OUTPUT_FETCHED_URLS_PATHFILE = os.path.join("data", "example.ural_results.csv")
List_of_Namedtuples = list[namedtuple]


def get_ural_result_object_from_fetched_urls(urls: list) -> List_of_Namedtuples:
    results = []
    for result in multithreaded_fetch(urls):
        results.append(result)
    return results


def report_unresponsive_urls(results: List_of_Namedtuples) -> list:
    return [result.url for result in results if not result.response]


def output_unresponsiveURLs(unresponsive_urls):
    with open(OUTPUT_UNRESPONSIVE_URLS_PATHFILE, "w", encoding="UTF8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["unresponsiveURL"])
        writer.writerows([unresponsive_urls])


def output_fetched_ural_data(results):
    output_filename = check_access_to_controlled_data()
    with open(output_filename, "w", encoding="UTF8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["item", "domain", "url", "error", "response", "meta"])
        writer.writerows([[result.item, result.domain, result.url, result.error, result.response, result.meta] 
            for result in results])


def check_access_to_controlled_data():
    if TestData.has_private_testdata:
        filepath = PRIVATE_OUTPUT_FETCHED_URLS_PATHFILE
    else:
        filepath = PUBLIC_OUTPUT_FETCHED_URLS_PATHFILE
    return filepath
