import json

import requests
import re

yellow = "\033[1;33m"
green = "\033[0;32m"
end = "\033[0m"


def request_data(source):
    print(f"{yellow}Requesting data from {end}{source} {yellow}...{end}")
    response = requests.get(source)
    if response:
        print(f"{green}Success{end}")
    return response


def load_data(response):
    return response.json()


def extract_url(json_data):
    return [
        url for url in \
        [article.get("claim-review", {}).get("itemReviewed", {}).get("appearance", {}).get("url") 
            for article in json_data.get("data")] 
        if url
        ]


def clean_urls(raw_urls):
    pattern_to_recover_good_domain = re.compile("\>\>(http.*)]]$")
    fixed_urls = [pattern_to_recover_good_domain.search(url).group(1) for url in raw_urls if pattern_to_recover_good_domain.search(url)]
    good_urls = [url for url in raw_urls if not pattern_to_recover_good_domain.search(url)]
    return fixed_urls+good_urls


def collect_urls(source):
    response = request_data(source)
    json_data = load_data(response)
    raw_urls = extract_url(json_data)
    return clean_urls(raw_urls)
