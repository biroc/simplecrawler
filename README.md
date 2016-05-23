# simplecrawler

A simple implementation of a multithreaded web crawler that extracts assets and links from each page it visits and constructs a sitemap.
It uses **Beautiful Soup 4** and **lxml** to parse html and look for specific elements, and **urllib** for downloading the page.

If present the robots.txt will be taken into account and possible rules are applied for each URL to consider if it should be added to the sitemap.
By default it also ignores .pdf and .xml extension.

## Installation

Clone the repository and install dependencies (preferably in a [virtualenv](https://virtualenvwrapper.readthedocs.io)) :
```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 crawl.py <domain_to_crawl>
```

Ouputting to a file:
```bash
python3 crawl.py <domain_to_crawl> > out.txt
```
Results will be in the following json format:

```json
{
   "Links": [
      "#start-of-content",
      "https://github.com/",
      "/personal",
      "/open-source",
      "/business",
      "/explore",
      "/join?source=header-home",
      "/login",
      "/pricing",
      "/blog",
      ...
   ],
   "Assets": [
      "https://assets-cdn.github.com/images/modules/site/home-ill-build.png?sn",
      "https://assets-cdn.github.com/images/modules/site/home-ill-work.png?sn",
      "https://assets-cdn.github.com/images/modules/site/home-ill-projects.png?sn",
      "https://assets-cdn.github.com/images/modules/site/home-ill-platform.png?sn",
      "https://assets-cdn.github.com/images/modules/site/org_example_nasa.png?sn",
      ...
   "URL": "http://github.com/"
}
```

## Design decisions

* Multi-threaded. Basic idea is that workers feed URLs to a multi-threaded priority queue which 'schedules' them to be parsed. For a quick implementation this is a relatively good choice for performance, as you don't have to wait for a result to continue crawling. The number of crawlers can be set at initialization.

* Compliant with robots.txt.

* Exclude recursive or duplicate crawls using 2 sets to maintain already visited nodes and exlcuded nodes (via robots.txt). Acess to sets synchronized by a [Lock](https://docs.python.org/3/library/threading.html#threading.Lock)

* Parser instead of  Regex to extract elements from HTML. Simply, regular expressions are not parsers, they are tools to find patterns.
If you want to find specific patterns use regex. HTML can be nested, malformed, and have other problems. There is a lot of discussion around this topic,
see [this](http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags/1732454#1732454) and [this](http://stackoverflow.com/questions/701166/can-you-provide-some-examples-of-why-it-is-hard-to-parse-xml-and-html-with-a-reg).

* [lxml](http://lxml.de/performance.html) as a [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) parser.

