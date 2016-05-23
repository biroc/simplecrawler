# simplecrawler

A simple implementation of a multithreaded web crawler that extracts assets and links from each page it visits and constructs a sitemap.
It uses **Beautiful Soup 4** and **lxml** to parse html and look for specific elements, and **urllib** for downloading the page.

If present the robots.txt will be taken into account and possible rules are applied for each URL to consider if it should be added to the sitemap.
By default it also ignores .pdf and .xml extension.

## Installation

Clone the repository and install dependencies (preferably in a [virtualenv](https://virtualenvwrapper.readthedocs.io)) :
```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 Simple_Crawler.py <domain_to_crawl>
```

Ouputting to a file:
```bash
python3 Simple_Crawler.py <domain_to_crawl> > out.txt
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
