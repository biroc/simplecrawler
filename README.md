# simplecrawler

This is a simple implementation of a multithreaded web crawler that extracts assets and links from each page it visits.
It uses **Beautiful Soup 4** and **lxml** to parse html and look for specific elements, and urllib for downloading the page.

If present the robots.txt will be taken into account and possible rules are applied for each URL to consider if it should be added to the sitemap.
By default it also ignored .pdf and .xml extension.
