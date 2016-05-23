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
            return

    def run(self):
        for i in range(self.no_crawlers):
            crawler = Crawler(i, self.queue, self.visited_urls, self.mutex, self.excluded, self.target_domain, self.robotparser)
            self.crawlers.append(crawler)
            crawler.start()

        self.queue.join()
        print("initial finish")
        for i in range(self.no_crawlers):
            self.queue.put(None)

        self.queue.join()
        for t in self.crawlers:
            t.join()
        print("Finished")


if __name__ == "__main__":
    domain = sys.argv[1]
    c = SimpleCrawler(domain=domain)
    c.start()
    c.join()
    print("Done")
