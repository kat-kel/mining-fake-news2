from collections import namedtuple
import trafilatura

from CONSTANTS import MINET_CONFG
from src_twitwi import twiwi_processing
from src_crowdtangle import crowdtangle_processing
from src_parsed_text_result import ParsedTextResult


domains_not_for_trafilatura = ["facebook.com", "twitter.com", "fb.watch", "youtube.com", "tiktok.com"]

def clean_fetch_results(raw_data:list[namedtuple]):
    return [data for data in raw_data 
            if data.response and data.response.status == 200
            and data.meta.get("encoding")]


def trafilatura_extraction_from_minet_meta(cleaned_results:list[namedtuple]):
    output = []
    for obj in cleaned_results:
        result = ParsedTextResult()
        result.FetchResult = obj
        if not any(domain == obj.domain for domain in domains_not_for_trafilatura):
            result.text = trafilatura.extract(obj.response.data.decode(obj.meta.get("encoding")))
        if result.text:
            output.append(result)
    return output


def twitter_extraction_from_minet_meta(cleaned_results:list[namedtuple]):
    if not MINET_CONFG:
        return
    else:
        tweet_objects = [obj for obj in cleaned_results if "twitter.com" == obj.domain]
        return twiwi_processing(tweet_objects)


def crowdtangle_extraction_from_minet_meta(cleaned_results:list[namedtuple]):
    if not MINET_CONFG:
        return
    else:
        facebook_objects = [obj for obj in cleaned_results if "facebook.com" == obj.domain]
        return crowdtangle_processing(facebook_objects)


def parse_text(raw_data:list[namedtuple]):
    cleaned_results = clean_fetch_results(raw_data)
    trafilatura_extract = trafilatura_extraction_from_minet_meta(cleaned_results)
    twitter_extract = twitter_extraction_from_minet_meta(cleaned_results)
    crowdtangle_extract = crowdtangle_extraction_from_minet_meta(cleaned_results)
    return trafilatura_extract + twitter_extract + crowdtangle_extract