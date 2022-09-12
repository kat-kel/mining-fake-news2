import json
import os

from src_data_collect import collect_urls, extract_url, clean_urls

PUBLIC_TESTDATA_FILENAME = os.path.join('data', 'example.response.json')
PRIVATE_TESTDATA_FILENAME = os.path.join('data', 'private.response.json')
PRIVATE_CONFIG_FILENAME = "private.config.json"

class TestData:
    has_public_testdata = os.path.isfile(PUBLIC_TESTDATA_FILENAME)
    has_private_config = os.path.isfile(PRIVATE_CONFIG_FILENAME)
    has_private_testdata = os.path.isfile(PRIVATE_TESTDATA_FILENAME)

    def get_data_source_url_from_config(self):
        """ Retrieve URL to the DeFacto data source, to test 
        the collect of fake news claims directly from DeFacto's site.

        Returns:
            string: the URL leading to the data source
        """        
        data_source = None
        if self.has_private_config:
            with open(PRIVATE_CONFIG_FILENAME, "r") as config_file:
                data_source = json.load(config_file).get("data_source")
            return data_source

    def extract_urls_from_data_source(self, to_request):
        """ Gather URLs of fake news articles, to test the processing of 
        URLs already stored in DeFacto's JSON data format.

        Args:
            to_request (bool): True value indicates the method should 
            send a request to DeFacto's API and receive new data in JSON format.

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
