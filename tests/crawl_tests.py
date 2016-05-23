import unittest
from Simple_Crawler import SimpleCrawler

class CrawlTestCase(unittest.TestCase):
    def test_bad_url(self):
        self.assertRaises(ValueError, SimpleCrawler, "http:")

    def test_no_crawlers(self):
        self.assertRaises(ValueError, SimpleCrawler, ["http://www.google.com", 0])
