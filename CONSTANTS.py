import os

PRIVATE_CONFIG_FILENAME = "private.config.json"
PUBLIC_TESTDATA_FILENAME = os.path.join('data', 'example.response.json')
PRIVATE_TESTDATA_FILENAME = os.path.join('data', 'private.response.json')
SMALL_URL_TEST_BATCH = os.path.join('data', 'example.urls.csv')
LARGE_URL_TEST_BATCH = os.path.join('data', 'private.urls.csv')
MINET_CONFG = os.path.join(".",".minetrc.yml")
CACHE_FILE = os.path.join(".", ".cache.csv")
PARSED_TEXT_FILE = os.path.join("data", "text.csv")
TEXT_FILE_FIELDNAMES = ["url", "domain", "message"]
CT_CACHE_FILEDNAMES = ["url", "message"]
CACHE_DIRECTORY = os.path.join(".", ".cache")