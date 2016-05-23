from threading import Thread
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from urllib import error
import os
from timeit import default_timer as timer

avoided_extensions = (".pdf", ".xml")

class Crawler(Thread):
    def __init__(self, crawlerID, queue, visited, mutex, excluded, target_domain, robotparser=None, crawls_done=0):
        Thread.__init__(self)
        self.crawlerID = crawlerID
        self.queue = queue
        self.visited = visited
        self.mutex = mutex
        self.excluded = excluded
        self.target_domain = target_domain
        self.robotparser = robotparser
        self.crawls_done = crawls_done

    def run(self):
        current = self.queue.get()
        while current != None:
            url = urlparse(current)
            try:
                response = urlopen(Request(current, headers={'User-Agent': 'Crawler'}))
                html = response.read()
                response.close()

                # Parse html using bs4 and lxml
                soup = BeautifulSoup(html, 'lxml')

                # Get links and assets
                links = [a.get('href') for a in soup.find_all('a')]
                assets = [element.get('src') for element in soup.find_all() if element.get('src') is not None]
                for l in links:
                    if not l:
                        continue

                    l, parsed, extension = clean_url(l, url)

                    # Ignore irrelevant links.
                    if parsed.scheme in ('mailto', 'tel', 'javascript'):
                        continue

                    # Check if link is outside domain.
                    if parsed.netloc != self.target_domain:
                        continue

                    # Ignore predefined extensions.
                    if extension in avoided_extensions:
                        continue

                    # Acquire mutex lock for this thread
                    # to check visited and excluded collections.
                    self.mutex.acquire()
                    # Check if link has not been visited, is about to be visited or is excluded.
                    if l in self.visited or l in self.excluded:
                        self.mutex.release()
                        continue

                    # Check to see if crawling is allowed by robots.txt
                    if self.robotparser and not self.robotparser.can_fetch('*', l):
                        self.excluded.add(l)
                        self.mutex.release()
                        continue

                    self.queue.put(l)
                    self.visited.add(l)
                    self.mutex.release()
            except Exception as e:
                print("Exception on url:" + url.geturl())

            self.queue.task_done()
            print(str(self.crawlerID) + " finished crawling " + url.geturl())
            current = self.queue.get()

        self.queue.task_done()


def clean_url(url, top_domain):
        if url.startswith('/'):
            url = 'http://' + top_domain.netloc + url
        elif url.startswith('#'):
            url = 'http://' + top_domain.netloc + top_domain.path + url
        elif not url.startswith('http') and not url.startswith(('mailto', 'tel', 'javascript')):
            url = 'http://' + top_domain.netloc + '/' + url

        if '#' in url:
            url = url[:url.index('#')]

        parsed = urlparse(url)
        extension = os.path.splitext(parsed.path)[1]

        return url, parsed, extension
