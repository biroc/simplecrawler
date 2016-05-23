from threading import Thread, Lock
from Crawler import Crawler
from queue import Queue
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from urllib import error


class SimpleCrawler(Thread):

    def __init__(self, domain, no_crawlers=10):
        Thread.__init__(self)
        # Set number of workers
        if no_crawlers < 1:
            raise ValueError("Must have at least 1 crawler")
        self.no_crawlers = no_crawlers
        # Multi-threaded priority queue to schedule crawling.
        self.queue = Queue()
        # Keep a set of visited urls to avoid recursive/ duplicate crawling
        self.visited_urls = set()
        # Keep a set of excluded urls.
        self.excluded = set()
        # Lock used to synchronize access to visited and exlucded sets/
        self.mutex = Lock()
        self.crawlers = []

        # Check if domain can be parsed and if robots.txt is present.
        if not domain:
            raise ValueError("Please provide a seed URL to crawl.")
        self.domain = domain
        try:
            self.target_domain = urlparse(domain).netloc
        except:
            raise ValueError("Incorrect URL")
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
        except Exception as e:
            raise ValueError("Incorrect URL or no robots.txt exists.")

        try:
            self.robotparser.read()
        except error.URLError:
            self.robotparser = None
            raise ValueError("Incorrect URL")
        except Exception as ex:
            self.robotparser = None
            raise ValueError("Incorrect URL or no robots.txt exists.")

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
