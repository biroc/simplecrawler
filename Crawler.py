from URLHelper import clean_url, valid_url
from Writer import output
from threading import Thread
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlparse


class Crawler(Thread):
    def __init__(self, crawlerID, queue, visited, mutex, excluded, target_domain, robotparser=None):
        Thread.__init__(self)
        self.crawlerID = crawlerID
        self.queue = queue
        self.visited = visited
        self.mutex = mutex
        self.excluded = excluded
        self.target_domain = target_domain
        self.robotparser = robotparser

    def run(self):
        current = self.queue.get()
        while current != None:
            url = urlparse(current)
            try:
                # Get page and html.
                response = urlopen(Request(current, headers={'User-Agent': 'Crawler'}))
                html = response.read()
                response.close()

                # Parse html using bs4 and lxml.
                soup = BeautifulSoup(html, 'lxml')

                # Get links and assets.
                links = [a.get('href') for a in soup.find_all('a')]
                assets = [element.get('src') for element in soup.find_all() if element.get('src') is not None]
                for l in links:
                    if not l:
                        continue

                    # Get parsed url and extension
                    l, parsed, extension = clean_url(l, url)

                    # Validate url.
                    if not valid_url(parsed, self.target_domain):
                        continue

                    # Acquire mutex lock for this thread.
                    self.mutex.acquire()

                    # Check if link is in visited and excluded collections.
                    if l in self.visited or l in self.excluded:
                        self.mutex.release()
                        continue

                    # Check to see if crawling is allowed by robots.txt
                    if self.robotparser and not self.robotparser.can_fetch('*', l):
                        self.excluded.add(l)
                        self.mutex.release()
                        continue

                    # Add link to queue and to visited set.
                    self.queue.put(l)
                    self.visited.add(l)

                    # Release lock.
                    self.mutex.release()

            except Exception as e:
                print("Exception on url:" + url.geturl())

            # Finished crawling from current url.
            # Notify that task is done.
            self.queue.task_done()

            # Output page info to sitemap.
            output(current, links, assets)

            # Get new task (url) to crawl.
            current = self.queue.get()

        # Last task executed by thread finished, notify.
        self.queue.task_done()
