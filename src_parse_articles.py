from collections import namedtuple
import trafilatura


def clean_fetch_results(raw_data:list[namedtuple]):
    clean_data = [data for data in raw_data 
            if data.response and data.response.status == 200
            and data.meta.get("encoding") == "utf-8"
            and data.meta.get("ext") == ".html"]
    return clean_data


def trafilatura_extraction_from_minet_meta(results:list[namedtuple]):
    data = clean_fetch_results(results)
    Output = namedtuple("Output", ["FetchResult", "text"])
    return [Output(obj, trafilatura.extract(obj.response.data.decode(obj.meta.get("encoding")))) 
            for obj in data
            if "facebook" not in obj.domain
            and "twitter" not in obj.domain
            and "fb.watch" not in obj.domain
            and "youtube" not in obj.domain]