from collections import Counter
import csv

from configure_data import TestData
from src_data_collect import collect_urls
from src_multithreaded_fetch import get_fetch_result_object
from src_parse_articles import trafilatura_extraction_from_minet_meta


# Open and parse the JSON data from De Facto
source = TestData().get_data_source_url_from_config()

# Extract a list of URLs to examine
if source:
    urls = collect_urls(source)
else:
    urls = TestData().extract_urls_from_test_batch(False)

# Fetch result objects from the URLs using Minet's multithreaded-fetch
result_objects = get_fetch_result_object(urls)

static_domains = [obj.domain for obj in result_objects]

count = dict(Counter(static_domains).most_common())

with open("data/test_domain_count.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "count"])
    for key,value in count.items():
        writer.writerow([key,value])
    