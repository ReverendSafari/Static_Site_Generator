import unittest
from copy_static import extract_title

class test_copy_static(unittest.TestCase):
    #Test no title
    def test_extract_error(self):
        title_md = "#No valid titles\n## Here boy"

        with self.assertRaises(ValueError):
            extract_title(title_md)

    #Test with title
    def test_extract_title(self):
        title_md = "# Valid TITLE BABY"
        self.assertEqual(extract_title(title_md), "Valid TITLE BABY")