import re
from collections import namedtuple

import minet.facebook as facebook
import yaml
from minet.crowdtangle.client import CrowdTangleAPIClient
from ural.facebook import FACEBOOK_DOMAIN_RE, is_facebook_url
from yaml.loader import SafeLoader

from CONSTANTS import MINET_CONFG

# --------------------------------------------------------#
#     HELPER FUNCTIONS
# --------------------------------------------------------#

# Open and parse the config file
def parse_config():
    with open(MINET_CONFG, "r") as config_file:
        config = yaml.load(config_file, Loader=SafeLoader)
    return config["crowdtangle"]


def call_client(client, url):
    post_id = facebook.post_id_from_url(url)
    if post_id:
        return client.post(post_id).message


# --------------------------------------------------------#
#     MAIN FUNCTION
# --------------------------------------------------------#

def crowdtangle_extract_text(fetch_objects, Output):
    output = []
    config = parse_config()
    client = CrowdTangleAPIClient(config["token"], config["rate_limit"])
    for obj in fetch_objects:
        if re.search(FACEBOOK_DOMAIN_RE, obj.domain):
            text = call_client(client, obj.url)
            if text:
                output.append(Output(FetchResult=obj, text=text))
    return output     


def new_crowdtangle_extract_text(fetch_objects, Output):
    config = parse_config()
    client = CrowdTangleAPIClient(config["token"], config["rate_limit"])
    return [
        result for result in
        [Output(obj, call_client(client, obj.url)) for obj in fetch_objects]
        if result.text
    ]
