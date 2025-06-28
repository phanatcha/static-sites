import unittest

from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):


    def test_title(self):
        md = "# Title"
        self.assertEqual(extract_title(md), "Title")

        md = "## Heading 2"
        with self.assertRaises(Exception):
            extract_title(md)

        md = "##### Heading 5"
        with self.assertRaises(Exception):
            extract_title(md)

        md = "Not a header"
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()