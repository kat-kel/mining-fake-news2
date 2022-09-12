import json
import unittest
from ural import get_domain_name
import os

from src_data_collect import request_data, load_data, extract_url, clean_urls
from configure_data import TestData

TESTDATA_FILENAME = os.path.join('data', 'example.response.json')
yellow = "\033[1;33m"
green = "\033[0;32m"
end = "\033[0m"


class Test_Request(unittest.TestCase):

    # Determine if the user has access to the controlled data
    no_access = not os.path.isfile("private.config.json")

    def __init__(self, source):
        super(Test_Request, self).__init__(source)
        print(f"\n{yellow}Setting up Tests...{end}")
        print("Getting data...")
        setup_data = TestData()
        self.source = setup_data.get_data_source_url_from_config()
    
    @unittest.skipIf(no_access,"skip")
    def setUp(self):
        self.response = request_data(self.source)

    @unittest.skipIf(no_access,"skip")
    def test_a_request_status(self):
        message = "Testing that the request was good..."
        print(f"\n{yellow}{message}{end}")
        status = self.response.status_code
        self.assertEqual(status,200)
        print(f"{green}Success{end}")
    
    @unittest.skipIf(no_access,"skip")
    def test_b_response_type(self):
        message = "Testing that the response is a JSON..."
        print(f"\n{yellow}{message}{end}")
        type = self.response.headers["content-type"]
        self.assertEqual(type,"application/json;charset=utf-8")
        print(f"{green}Success{end}")
    
    @unittest.skipIf(no_access,"skip")
    def test_c_load_data(self):
        message = "Testing that Python loaded the JSON response as a dictionary..."
        print(f"\n{yellow}{message}{end}")
        loaded_data = load_data(self.response)
        self.assertIsInstance(loaded_data, dict)
        print(f"{green}Success{end}")


class Test_JSON_Parsing(unittest.TestCase):

    def setUp(self):
        with open(TESTDATA_FILENAME, 'r') as f:
            self.testdata = json.load(f)
            self.raw_urls = extract_url(self.testdata)
            self.clean_urls = clean_urls(self.raw_urls)

    def test_1_extract_urls(self):
        message = "Testing that the URLs are in a list..."
        print(f"\n{yellow}{message}{end}")
        self.assertIsInstance(self.raw_urls, list)
        print(f"{green}Success{end}")
    
    def test_2_no_url_is_None(self):
        message = "Testing that no URL is  None..."
        print(f"\n{yellow}{message}{end}")
        self.assertNotIn(None, self.raw_urls)
        print(f"{green}Success{end}")
    
    def test_3_valid_domain_name(self):
        message = "Testing that every URL has a valid domain name..."
        print(f"\n{yellow}{message}{end}")
        checked_urls = [get_domain_name(url) for url in self.clean_urls]
        self.assertIsInstance(checked_urls, list)
        self.assertNotIn(None, checked_urls)
        print(f"{green}Success{end}")


if __name__ == "__main__":
    unittest.main()
