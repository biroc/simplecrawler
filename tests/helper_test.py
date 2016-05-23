import unittest
from URLHelper import valid_url, clean_url
from urllib.parse import urlparse

class URLTestCase(unittest.TestCase):
    def setUp(self):
        self.scheme_url = urlparse('mailto:somemail@gmail.com')
        self.domain_url = urlparse('http://www.facebook.com')
        self.extension_url = urlparse('http://somepage.com/name.pdf')

    def test_scheme(self):
        self.assertFalse(valid_url(self.scheme_url, 'www.google.com'))

    def test_domain(self):
        self.assertFalse(valid_url(self.domain_url,'gocardless.com'))

    def test_extension(self):
        self.assertFalse(valid_url(self.extension_url,'somepage.com'))

