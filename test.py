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
        cache = fetch.Cache()
        self.assertIsInstance(cache.size, int)

    def test_get_headers(self):
        headers = {"Accept": "application/json", "User-Agent": "Mozilla/5.0"}
        content = fetch.get("http://headers.jsontest.com/", headers=headers)
        self.assertIsInstance(content, str)
        data = json.loads(content)
        self.assertTrue(headers.items() <= data.items())

    def test_get_basic_auth(self):
        credentials = ("username", "password")
        expected_header_tuple = (
            'Authorization', 'Basic dXNlcm5hbWU6cGFzc3dvcmQ=')
        self.assertEqual(fetch.basicAuthHeader(
            credentials), expected_header_tuple)
        content = fetch.get("http://time.jsontest.com/",
                            auth=("user", "password"))
        self.assertIsInstance(content, str)


if __name__ == '__main__':
    unittest.main()
