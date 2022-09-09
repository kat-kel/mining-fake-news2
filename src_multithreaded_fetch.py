import csv
import os

from minet import multithreaded_fetch

OUTPUT_PATHFILE = os.path.join("data", "unresponsiveURL.csv")


def report_unresponsive_urls(urls):
    unresponsive_urls = []
    for result in multithreaded_fetch(urls):
        if result.response is None:
            unresponsive_urls.append(result.url)
    return unresponsive_urls


def output_unresponsiveURLs(unresponsive_urls):
    with open(OUTPUT_PATHFILE, "w", encoding="UTF8") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["unresponsiveURL"])
        writer.writerows([unresponsive_urls])
