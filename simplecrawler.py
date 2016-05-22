from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from urllib import error
import os

robots = "robots.txt"
avoided_extensions = (".pdf", ".xml")


class Crawler():

    def __init__(self, domain=""):
        self.domain = domain
        self.target_domain = urlparse(domain).netloc

        self.set_robot_parser()

        self.queue = {domain}
        self.visited = set([])
        self.excluded = set([])
        self.no_visited = 1

    def set_robot_parser(self):
        if self.domain[-1] != "/":
            self.domain += "/"
        self.robotparser = RobotFileParser()
        self.robotparser.set_url(self.domain + robots)
        self.robotparser.read()

    def start(self):
        while self.queue:
            self.__crawl()

    def __crawl(self):
        current = self.queue.pop()
        self.visited.add(current)

        url = urlparse(current)
        try:
            response = urlopen(Request(current, headers={"User-Agent": "Crawler"}))
        except error.HTTPError:
            return

        try:
            html = response.read()
            response.close()
        except Exception as e:
            return

        soup = BeautifulSoup(html, 'lxml')
        links = [a.get('href') for a in soup.find_all('a')]
        assets = [element.get('src') for element in soup.find_all() if element.get('src') is not None]
        print(assets)
        print(url.geturl() + ":")
        for l in links:
            if not l:
                continue

            l, parsed, extension = Crawler.clean_url(l)

            # Check if link has not been visited, is about to be visited or is excluded.
            if l in self.queue or l in self.visited or l in self.excluded:
                continue

            # Check if link is outside domain.
            if parsed.netloc != self.target_domain:
                continue

            # Ignore irrelevant links.
            if parsed.scheme in ('mailto', 'tel', 'javascript'):
                continue

            # Ignore predefined extensions.
            if extension in avoided_extensions:
                continue

            # Check to see if crawling is allowed by robots.txt
            if self.robotparser and not self.robotparser.can_fetch("*", l):
                self.excluded.add(l)
                continue

            print(l)
            self.no_visited += 1
            print(self.no_visited)
            self.queue.add(l)

    @staticmethod
    def clean_url(url):
            if url.startswith('/'):
                url = "http://" + url.netloc + url
            elif url.startswith("#"):
                url = "http://" + url.netloc + url.path + url
            elif not url.startswith("http"):
                url = "http://" + url.netloc + "/" + url

            if "#" in url:
                url = url[:url.index("#")]

            parsed = urlparse(url)
            extension = os.path.splitext(parsed.path)[1]

            return url, parsed, extension

c = Crawler("http://gocardless.com")
c.start()