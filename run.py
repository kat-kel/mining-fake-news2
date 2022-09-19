from configure_data import TestData
from src_data_collect import collect_urls
from src_multithreaded_fetch import get_fetch_result_object
from src_parse_articles import trafilatura_extraction_from_minet_meta
import os


# Open and parse the JSON data from De Facto
source = TestData().get_data_source_url_from_config()

# Extract a list of URLs to examine
if source:
    urls = collect_urls(source)
else:
    urls = TestData().extract_urls_from_test_batch(False)

# Fetch result objects from the URLs using Minet's multithreaded-fetch
fetch_result_objects = get_fetch_result_object(urls)

# Extract text from the result objects using Trafilatura
parsed_fetch_results = trafilatura_extraction_from_minet_meta(fetch_result_objects)

#Output text
for i, obj in enumerate(parsed_fetch_results):
    with open (os.path.join("data", "text", f"{i}{obj.FetchResult.domain}.txt"), "w") as f:
        f.write(obj.text)