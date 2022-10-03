import tracemalloc
import unittest

from configure_data import TestData
from src_clean_text import (
    remove_invalid_text,
    split_sentences
)

yellow = "\033[1;33m"
green = "\033[0;32m"
end = "\033[0m"

class Test_clean_extracted_text(unittest.TestCase):

    def setUp(self):
        self.text = TestData().parse_extracted_text()

    def test_remove_invalid_text(self):
        valid_texts = remove_invalid_text(self.text)
        self.assertGreaterEqual(len(self.text), len(valid_texts))
    
    def test_split_sentences(self):
        valid_texts = remove_invalid_text(self.text)
        sentences = split_sentences(valid_texts)
        for i, sentence in enumerate(sentences):
            if i < 5:
                print(sentence)




if __name__ == "__main__":
    tracemalloc.start()
    unittest.main()
