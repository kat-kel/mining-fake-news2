import re

import yaml
from twitwi import (
    TwitterWrapper, 
    normalize_tweets_payload_v2
)
from yaml.loader import SafeLoader

from CONSTANTS import MINET_CONFG
BATCH_SIZE = 50


# --------------------------------------------------------#
#     HELPER FUNCTIONS
# --------------------------------------------------------#

# Open and parse the config file
def parse_config():
    with open(MINET_CONFG, "r") as config_file:
        config = yaml.load(config_file, Loader=SafeLoader)
    return config["twitter"]


# Divide the FetchObject into batches
def divide_into_batches(all_fetch_results, batch_size):
    return [
        all_fetch_results[x:x+batch_size] 
        for x 
        in range(0, len(all_fetch_results), batch_size)
    ]


# Extract a FetchObject's ID from the URL
def get_id(obj):
    pattern = re.compile(r"status\/([0-9]+)")
    result = re.search(pattern, obj.url)
    if result and result.group(1):
        return result.group(1)


# Create a list of valid Tweet IDs
def joined_ids(batch):
    tweet_objects_with_id = []
    for obj in batch:
        id = (get_id(obj))
        if id:
            tweet_objects_with_id.append({"id": id, "FetchObject": obj})
    return tweet_objects_with_id


def combine_normalized_tweet_and_fetch_object(tweet_objects_with_id, normalized_tweets, Output):
    output = []
    for obj in tweet_objects_with_id:
        matched_normalized_tweet = list(filter(lambda tweet: tweet["id"] == obj["id"], normalized_tweets))
        if matched_normalized_tweet:
            output.append(Output(FetchResult=obj["FetchObject"], text=matched_normalized_tweet[0]["text"]))
    return output

    
# Send a list of ids to the Twitter API
def call_client(wrapper, batch, Output):
    # params taken from: https://github.com/python-twitter-tools/twitter/tree/api_v2
    v2_params={
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
        "user.fields":  "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,attachments.poll_ids,attachments.media_keys,in_reply_to_user_id,geo.place_id"
        }
    # Parse the ID for each tweet in the batch
    tweet_objects_with_id = joined_ids(batch)
    # Call the API for all the tweets in the batch 
    result = wrapper.call(["tweets"], 
                            ids=",".join(item["id"] for item in tweet_objects_with_id), 
                            params=v2_params)
    # Normalize the tweets returned from the API
    normalized_tweets = normalize_tweets_payload_v2(result, collection_source="api")
    # By tweet ID, combine the normalized tweets with the original FetchResult object
    fetch_objects_with_tweets = combine_normalized_tweet_and_fetch_object(tweet_objects_with_id, normalized_tweets, Output)
    return fetch_objects_with_tweets


# --------------------------------------------------------#
#     MAIN FUNCTION
# --------------------------------------------------------#
def twiwi_processing(fetch_objects, Output):
    config = parse_config()

    # Set up the wrapper with config details
    wrapper = TwitterWrapper(
        config["access_token"],
        config["access_token_secret"],
        config["api_key"],
        config["api_secret_key"],
        listener=None,
        api_version="2"
    )
    
    # Divide the tweets up in batches with a maxiumum length of 3
    batches = divide_into_batches(fetch_objects, BATCH_SIZE)

    return [
        item for batch in
        [call_client(wrapper, batch, Output) for batch in batches]
        for item in batch
        ]