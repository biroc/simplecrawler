from threading import Thread, Lock
from Crawler import Crawler
from queue import Queue
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
import sys

class SimpleCrawler(Thread):

    def __init__(self, no_crawlers=10, domain=""):
        Thread.__init__(self)
        self.no_crawlers = no_crawlers
        self.queue = Queue()
        self.visited_urls = set()
        self.mutex = Lock()
        self.crawlers = []
        self.excluded = set()
        self.domain = domain
        try:
            self.target_domain = urlparse(domain).netloc
        except:
            raise Exception('Invalid url provided.')
        self.set_robot_parser()
        self.queue.put(self.domain)
        self.visited_urls.add(self.domain)

    def set_robot_parser(self):
        """
        Given a domain tries to search for /robots.txt and identify which urls should
        not be visited by the crawler.
        """
        if self.domain[-1] != '/':
            self.domain += '/'
        self.robotparser = RobotFileParser()
        try:
            self.robotparser.set_url(self.domain + "robots.txt")
        except:
            raise Exception('Invalid url or no robots.txt exists.')

        try:
            self.robotparser.read()
        except:
            self.robotparser = None
            raise Exception('Invalid url or no robots.txt exists.')

    def run(self):

        # Spawn threads and start crawling.
        for i in range(self.no_crawlers):
            crawler = Crawler(i, self.queue, self.visited_urls, self.mutex, self.excluded, self.target_domain, self.robotparser)
            self.crawlers.append(crawler)
            crawler.start()

        # Wait for all crawlers to finish.
        self.queue.join()

        # Notify all crawlers to stop.
        for i in range(self.no_crawlers):
            self.queue.put(None)

        self.queue.join()

        # Wait for all threads to exit
        for t in self.crawlers:
            t.join()


if __name__ == "__main__":
    domain = sys.argv[1]
    c = SimpleCrawler(domain=domain)
    c.start()
    c.join()
    # Done
