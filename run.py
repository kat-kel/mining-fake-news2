import csv

from configure_data import TestData
from CONSTANTS import PARSED_TEXT_FILE
from src_data_collect import collect_urls
from src_multithreaded_fetch import get_fetch_result_object
from src_parse_articles import parse_text

# Open and parse the JSON data from De Facto
source = TestData().get_data_source_url_from_config()

# Extract a list of URLs to examine
if source:
    urls = collect_urls(source)
else:
    urls = TestData().extract_urls_from_test_batch("small")

# Fetch result objects from the URLs using Minet's multithreaded-fetch
fetch_result_objects = get_fetch_result_object(urls)

# Extract text from the result objects using Trafilatura
parsed_text = parse_text(fetch_result_objects)

#Output text
with open (PARSED_TEXT_FILE, "w") as f:
    fieldnames = ["url", "message"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    for item in parsed_text:
        writer.writerow({"url": item.FetchResult.url, "message": item.text})
