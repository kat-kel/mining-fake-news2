from collections import namedtuple
import trafilatura


def trafilatura_extraction_from_minet_meta(result_objects:list[namedtuple]):
    output = []
    for i, obj in enumerate(result_objects):
        encoding = obj.meta.get("encoding")
        extract = trafilatura.extract(obj.response.data.decode(encoding), target_language="fr")
        output.append(extract)
        # Output extraction for each sample
        with open(f"data/test_{i}{obj.domain}_trafilatura.txt", "w") as f:
            f.write(extract)
    return output

    # goal:
    #return [trafilatura.extract(obj.response.data.decode(encoding), target_language="fr") for obj in result_objects]


def trafilatura_extraction_from_url(result_objects:list[namedtuple]):
    output = []
    for obj in result_objects:
        extract = trafilatura.extract(trafilatura.fetch_url(obj.url), target_language="fr")
        output.append(extract)
        if extract=="! D O C T Y P E h t m l >":
            print(f"\n\nFor the domain {obj.domain}, the text is:\n{extract}")
    return output