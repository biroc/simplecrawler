from Simple_Crawler import SimpleCrawler
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Format: python3 crawl.py <domain>")
    else:
        domain = sys.argv[1]
        c = SimpleCrawler(domain=domain)
        c.start()
        c.join()
        print("Finished")
