import csv
import json
import os

from CONSTANTS import (
    PRIVATE_CONFIG_FILENAME, 
    PUBLIC_TESTDATA_FILENAME, 
    PRIVATE_TESTDATA_FILENAME, 
    SMALL_URL_TEST_BATCH, 
    LARGE_URL_TEST_BATCH,
    PARSED_TEXT_FILE
)
from src_data_collect import (
    clean_urls, 
    collect_urls, 
    extract_url
)


class TestData:
    has_public_testdata = os.path.isfile(PUBLIC_TESTDATA_FILENAME)
    has_private_config = os.path.isfile(PRIVATE_CONFIG_FILENAME)
    has_private_testdata = os.path.isfile(PRIVATE_TESTDATA_FILENAME)
    has_small_url_test_batch = os.path.isfile(SMALL_URL_TEST_BATCH)
    has_large_url_test_batch = os.path.isfile(LARGE_URL_TEST_BATCH)
    has_parsed_text_file = os.path.isfile(PARSED_TEXT_FILE)

    def get_data_source_url_from_config(self):
        """ Call the API to De Facto's database and retrieve a JSON response.

        Returns:
            string: the URL leading to the data source
        """        
        data_source = None
        if self.has_private_config:
            with open(PRIVATE_CONFIG_FILENAME, "r") as config_file:
                data_source = json.load(config_file).get("data_source")
            return data_source

    def extract_urls_from_data_source(self, to_request:bool):
        """ Parse URLs from the JSON format of De Facto's data.

        Args:
            to_request (bool): True value indicates the method should send a request to De Facto's API and receive new data in JSON format.

        Returns:
            list: list of URLs to fake news articles
        """        
        if self.has_private_config and to_request:
            data_source = self.get_data_source_url_from_config()
            self.urls = collect_urls(data_source)
        elif self.has_private_testdata:
            with open(PRIVATE_TESTDATA_FILENAME, "r") as f:
                data = json.load(f)
                self.urls = clean_urls(extract_url(data))
        elif self.has_public_testdata:
            with open(PUBLIC_TESTDATA_FILENAME, "r") as f:
                testdata = json.load(f)
                self.urls = clean_urls(extract_url(testdata))
        else:
            raise OSError("JSON test data was not found.")
        return self.urls
    
    def extract_urls_from_test_batch(self, batch):
        """ Parse URLs from a static CSV file of test data.

        Args:
            batch (str): "large" parses a large file of private data from De Facto, "small" parses a small file of public example data.

        Returns:
            list: list of URLs to fake news articles
        """
        if batch == "small" and self.has_small_url_test_batch:
            batch = SMALL_URL_TEST_BATCH
        elif batch == "large" and self.has_large_url_test_batch:
            batch = LARGE_URL_TEST_BATCH
        else:
            batch = None
            raise OSError("Sample of URLs was not found.")
        if batch:
            with open(batch, "r", encoding="utf8") as f:
                reader = csv.reader(f)
                return [item for sublist in list(reader) 
                        for item in sublist]
    
    def parse_extracted_text(self):
        if self.has_parsed_text_file:
            with open(PARSED_TEXT_FILE, "r") as csvfile:
                return [row for row in csv.DictReader(csvfile)]
        else:
            raise OSError("The file of extracted text was not found.")
