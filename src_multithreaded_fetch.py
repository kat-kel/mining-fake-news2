from collections import namedtuple

from minet import multithreaded_fetch

ListOfNamedtuples = list[namedtuple]


def get_fetch_result_object(urls: list) -> ListOfNamedtuples:
    results = []
    for result in multithreaded_fetch(urls):
        results.append(result)
    return results

def report_domain_names(results: ListOfNamedtuples) -> list:
    return [result.domain for result in results if not result.response]
