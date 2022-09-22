import re

import yaml
from twitwi import TwitterWrapper, normalize_tweets_payload_v2
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


# Get the user ID from within one twitter URL
def get_id(obj):
    pattern = re.compile(r"status\/([0-9]+)")
    result = re.search(pattern, obj.url)
    if result.group(1):
        return result.group(1)


# Divide the ResultObjects into batches
def divide_into_batches(all_fetch_results, batch_size):
    return [
        all_fetch_results[x:x+batch_size] 
        for x 
        in range(0, len(all_fetch_results), batch_size)
    ]


# Send a list of ids to the Twitter API
def call_client(wrapper, ids):
    # params taken from: https://github.com/python-twitter-tools/twitter/tree/api_v2
    v2_params={
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
        "user.fields":  "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,attachments.poll_ids,attachments.media_keys,in_reply_to_user_id,geo.place_id"
        }
    result = wrapper.call(["tweets"], 
                            ids=ids, 
                            params=v2_params)
    normalized_tweets = normalize_tweets_payload_v2(result, collection_source="api")
    return normalized_tweets


# --------------------------------------------------------#
#     MAIN FUNCTION
# --------------------------------------------------------#
def get_tweet_text(fetch_objects, Output):
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
    
    # For each batch, call the client and add the results to output
    normalized_tweets = [
        normalized_tweet for batch_of_normalized_tweets in
        [   call_client(wrapper, ",".join( [get_id(obj) 
                                            for obj in batch
                                            ])) 
            for batch in batches
        ]
        for normalized_tweet in batch_of_normalized_tweets
    ]
    
    # Return an Output object with all the data from the input FetchResult 
    # along with the text extracted from the normalized tweet
    return [Output( FetchResult=fetch_objects[index], 
                    text=normalized_tweets[index]["text"]
                )
            for index in range(len(fetch_objects))
    ]
