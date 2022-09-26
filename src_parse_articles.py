from collections import namedtuple
import trafilatura

from CONSTANTS import MINET_CONFG
from src_twitwi import get_tweet_text
from src_crowdtangle import crowdtangle_extract_text


domains_not_for_trafilatura = ["facebook.com", "twitter.com", "fb.watch", "youtube.com", "tiktok.com"]
Output = namedtuple("Output", ["FetchResult", "text"])

def clean_fetch_results(raw_data:list[namedtuple]):
    return [data for data in raw_data 
            if data.response and data.response.status == 200]


def trafilatura_extraction_from_minet_meta(cleaned_results:list[namedtuple]):
    return [Output(obj, trafilatura.extract(obj.response.data.decode(obj.meta.get("encoding")))) 
            for obj in cleaned_results
            if not any(domain == obj.domain for domain in domains_not_for_trafilatura)]


def twitter_extraction_from_minet_meta(cleaned_results:list[namedtuple]):
    if not MINET_CONFG:
        return
    else:
        tweet_objects = [obj for obj in cleaned_results if "twitter.com" == obj.domain]
        return get_tweet_text(tweet_objects, Output)


def crowdtangle_extraction_from_minet_meta(cleaned_results:list[namedtuple]):
    if not MINET_CONFG:
        return
    else:
        facebook_objects = [obj for obj in cleaned_results if "facebook.com" == obj.domain]
        return crowdtangle_extract_text(facebook_objects, Output)
        