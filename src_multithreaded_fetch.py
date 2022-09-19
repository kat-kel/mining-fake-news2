from collections import namedtuple

from minet import multithreaded_fetch

ListOfNamedtuples = list[namedtuple]
yellow = "\033[1;33m"
green = "\033[0;32m"
end = "\033[0m"


def get_fetch_result_object(urls: list) -> ListOfNamedtuples:
    results = []
    print(f"{yellow}Fetching results from {len(urls)} URLs...{end}")
    for result in multithreaded_fetch(urls):
        results.append(result)
    return results

