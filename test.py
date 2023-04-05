import unittest
import fetch
import json

class TestFetch(unittest.TestCase):

    def test_get_jsonecho(self):
        content = fetch.get("http://echo.jsontest.com/key/value/one/two")
        reference = {"key": "value", "one": "two"}
        self.assertEqual(json.loads(content), reference, "json echo failed")

    def test_fetch(self):
        content = fetch.fetch("http://ip.jsontest.com")
        self.assertIsInstance(content, str)
        self.assertIsInstance(json.loads(content), dict)

    def test_cache_usage(self):
        size = fetch.cache_usage()
        self.assertIsInstance(size, int)



if __name__ == '__main__':
    unittest.main()