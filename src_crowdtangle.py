import csv

import minet.facebook as facebook
import yaml
from minet.crowdtangle.client import CrowdTangleAPIClient
from minet.crowdtangle.exceptions import CrowdTanglePostNotFound
from yaml.loader import SafeLoader

from CONSTANTS import (
    CACHE_FILE, 
    MINET_CONFG
)

# --------------------------------------------------------#
#     HELPER FUNCTIONS
# --------------------------------------------------------#

# Open and parse the config file
def parse_config():
    with open(MINET_CONFG, "r") as config_file:
        config = yaml.load(config_file, Loader=SafeLoader)
    return config["crowdtangle"]


# Open and parse the current cache file
def open_cache():
    with open(CACHE_FILE, "r") as f:
        return [row for row in csv.DictReader(f)]


# Update the cache object and rewrite the cache file
def rewrite_cache(cache, url, message):
    # Update cache with new URL and message
    cache.append({"url":url, "message":message})
    with open(CACHE_FILE, "w") as f:
        fieldnames = ["url", "message"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for row in cache:
            writer.writerow(row)


# Call the CrowdTangle API
def call_client(client, url):
    post_id = facebook.post_id_from_url(url)
    if post_id:
        try:
            post = client.post(post_id)
            return post.message    
        except CrowdTanglePostNotFound as error:
            print(repr(error))


# Check if the URL has already been called / is in the cache.
# Otheriwse, call the client and update the cache.
def check_cache(client, url, cache):
    cached_url = list(filter(lambda entry: entry["url"] == url, cache))
    if cached_url and len(cached_url) == 1:
        return cached_url[0]["message"]
    else:
        message = call_client(client, url)
        rewrite_cache(cache, url, message)
        return message


# --------------------------------------------------------#
#     MAIN FUNCTION
# --------------------------------------------------------#

def crowdtangle_extract_text(fetch_objects, Output):
    config = parse_config()
    client = CrowdTangleAPIClient(config["token"], config["rate_limit"])
    cache = open_cache()
    return [
        result for result in
        [Output(obj, check_cache(client, obj.url, cache)) for obj in fetch_objects]
        if result.text
    ]
