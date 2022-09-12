import json
import os

from src_data_collect import collect_urls, extract_url, clean_urls

PUBLIC_TESTDATA_FILENAME = os.path.join('data', 'example.response.json')
PRIVATE_TESTDATA_FILENAME = os.path.join('data', 'private.response.json')
PRIVATE_CONFIG_FILENAME = "private.config.json"

class URLs:
    # Determine if the user has access to a private configuration file
    has_private_config = os.path.isfile(PRIVATE_CONFIG_FILENAME)

    # FOR TESTING THE COLLECT OF FAKE NEWS CLAIMS DIRECTLY FROM THE DATA SOURCE
    def get_data_source_url_from_config(self):
        """Deserialize the config JSON and retrieve the URL that links 
            to a source of fake new claims.

        Returns:
            string: the URL leading to the data source
        """        
        data_source = None
        if self.has_private_config:
            with open(PRIVATE_CONFIG_FILENAME, "r") as config_file:
                data_source = json.load(config_file).get("data_source")
            return data_source

    # FOR TESTING THE PROCESSING OF FAKE NEWS URLS (ALREADY PARSED FROM THE DATA SOURCE)
    def extract_urls_from_data_source(self, to_request):
        """Extract a list of URLs from the JSON data, 
            either by (1) directly opening a JSON stored locally 
            (2) or requesting the JSON from an API. The approach 
            depends on whether a request is desired (to_request).

        Args:
            to_request (bool): True value indicates the method should 
            send a request to the API and receive the data in JSON format.

        Returns:
            list: list of URLs to fake news claims
        """        
        if self.has_private_config:
            if to_request:
                data_source = self.get_data_source_url_from_config()
                self.urls = collect_urls(data_source)
            else:
                with open(PRIVATE_TESTDATA_FILENAME, "r") as f:
                    data = json.load(f)
                    self.urls = clean_urls(extract_url(data))
        else:
            with open(PUBLIC_TESTDATA_FILENAME, "r") as f:
                self.testdata = json.load(f)
                self.urls = clean_urls(extract_url(self.testdata))
        return self.urls


if __name__ == "__main__":
    test = URLs()
    print(test.private_config)