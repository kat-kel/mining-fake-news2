import unittest
import os
import tracemalloc

from configure_data import TestData
from src_multithreaded_fetch import get_fetch_result_object
from src_parse_articles import trafilatura_extraction_from_minet_meta

TESTDATA_FILENAME = os.path.join('data', 'example.response.json')
yellow = "\033[1;33m"
green = "\033[0;32m"
end = "\033[0m"


class Test_URL_Response(unittest.TestCase):

    def setUp(self):
        print(f"\n{yellow}Setting up Tests...{end}")
        print("Getting the URLs...")
        self.urls = TestData().extract_urls_from_test_batch("small")

    def test_extract_from_meta(self):
        message = f"Testing multithreaded fetch..."
        print(f"\n{yellow}{message}{ end}")
        result_objects = get_fetch_result_object(self.urls)
        output = trafilatura_extraction_from_minet_meta(result_objects)
        print(output)
        print(f"{green}Success{end}")
        
    
if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()