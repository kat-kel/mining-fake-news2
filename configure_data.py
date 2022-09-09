import json
import os

from src_data_collect import collect_urls, extract_url, clean_urls

TESTDATA_FILENAME = os.path.join('data', 'example.response.json')

class URLs:

    def open_private_config(self):
        if os.path.isfile("private.config.json"):
            with open("private.config.json", "r") as config_file:
                data_source = json.load(config_file).get("data_source")
        return data_source

    def get_urls(self, to_request):
        # If access to controlled data
        if self.open_private_config():
            if to_request:
                data_source = self.open_private_config()
                self.urls = collect_urls(data_source)
            else:
                with open("data/private.response.json", "r") as f:
                    data = json.load(f)
                    self.urls = clean_urls(extract_url(data))
        # Otherwise, use fake URLs
        else:
            with open(TESTDATA_FILENAME, "r") as f:
                self.testdata = json.load(f)
                self.urls = clean_urls(extract_url(self.testdata))

        return self.urls

    def get_source(self):
        if self.open_private_config():
            return self.open_private_config()

