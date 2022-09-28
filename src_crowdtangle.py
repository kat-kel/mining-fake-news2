import csv
import os
from hashlib import md5

import minet.facebook as facebook
import yaml
from minet.crowdtangle.client import CrowdTangleAPIClient
from minet.crowdtangle.exceptions import CrowdTanglePostNotFound
from yaml.loader import SafeLoader

from CONSTANTS import (
    CACHE_DIRECTORY,
    CT_CACHE_FILEDNAMES,
    MINET_CONFG,
)

from src_parsed_text_result import ParsedTextResult

# --------------------------------------------------------#
#     MAIN FUNCTION
# --------------------------------------------------------#

def crowdtangle_processing(fetch_objects):
    output = []
    config = read_config()
    if config:
        client = CrowdTangleAPIClient(config["token"], config["rate_limit"])
        for obj in fetch_objects:
            result = ParsedTextResult()
            result.FetchResult = obj
            if in_cache(obj):
                result.text = parse_cache_file(obj)
            else:
                result.text = call_client(client, obj.url)
                add_to_cache(result)
            if result.text:
                output.append(result)
    return output


# --------------------------------------------------------#
#     HELPER FUNCTIONS TO PROCESS PYTHON OBJECTS
# --------------------------------------------------------#

# Hash the URL.
def hash_url(url):
    return md5(str.encode(url)).hexdigest()


# Check if the URL's hash is the name of a file in the cache directory.
def in_cache(obj):
    if not os.path.isdir(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)
    cached_hashes = os.listdir(CACHE_DIRECTORY)
    hashed_url = hash_url(obj.url)
    return hashed_url in cached_hashes


# Call the CrowdTangle API.
def call_client(client, url):
    post_id = facebook.post_id_from_url(url)
    if post_id:
        try:
            post = client.post(post_id)
            return post.message    
        except CrowdTanglePostNotFound as error:
            print(repr(error))


# --------------------------------------------------------#
#     READ/WRITE EXTERNAL FILES
# --------------------------------------------------------#

# Open and parse the config file.
def read_config():
    if os.path.isfile(MINET_CONFG):
        with open(MINET_CONFG, "r") as config_file:
            config = yaml.load(config_file, Loader=SafeLoader)
            if config["crowdtangle"]:
                return config["crowdtangle"]


# Write a cache file for the processed URL.
def add_to_cache(result):
    cache_file = os.path.join(CACHE_DIRECTORY, hash_url(result.FetchResult.url))
    with open(cache_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=CT_CACHE_FILEDNAMES)
        writer.writeheader()
        writer.writerow({
            CT_CACHE_FILEDNAMES[0]: result.FetchResult.url, 
            CT_CACHE_FILEDNAMES[1]: result.text
        })


# Parse a preexisting cache file to get the Facebook post's message.
def parse_cache_file(obj):
    cache_file = os.path.join(CACHE_DIRECTORY, hash_url(obj.url))
    with open(cache_file, "r") as f:
        reader = csv.DictReader(f)
        message = next(reader)[CT_CACHE_FILEDNAMES[1]]
        if message:
            return message
