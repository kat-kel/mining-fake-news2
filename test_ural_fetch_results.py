import unittest
import os
import tracemalloc

from configure_data import TestData
from src_multithreaded_fetch import get_ural_result_object_from_fetched_urls, output_fetched_ural_data

TESTDATA_FILENAME = os.path.join('data', 'example.response.json')
MINIMUM_SUCCESS_RATE = 0.98
yellow = "\033[1;33m"
green = "\033[0;32m"
end = "\033[0m"


class Test_URL_Response(unittest.TestCase):

    def setUp(self):
        print(f"\n{yellow}Setting up Tests...{end}")
        print("Getting the URLs...")
        setup_data = TestData()
        self.urls = setup_data.extract_urls_from_data_source(False) # do not request JSON from online, use local file
        print(f"    Working with {len(self.urls)} URLs.")
        print("Getting responses...")
        self.fetch_results = get_ural_result_object_from_fetched_urls(self.urls)

    def test_write_fetched_ural_data(self):
        message = f"Generating a new output file of all fetched URAL data..."
        print(f"\n{yellow}{message}{end}")
        output_fetched_ural_data(self.fetch_results)
        print(f"{green}Success{end}")

    
if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
