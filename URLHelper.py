from urllib.parse import urlparse
import os

avoided_extensions = (".pdf", ".xml")


def clean_url(url, top_domain):
    """
    Given a path construct full URL with top level domain.
    Return full url, parsed url, and extension.
    """
    if url.startswith('/'):
        url = 'http://' + top_domain.netloc + url
    elif url.startswith('#'):
        url = 'http://' + top_domain.netloc + top_domain.path + url
    elif not url.startswith('http') and not url.startswith(('mailto', 'tel', 'javascript')):
        url = 'http://' + top_domain.netloc + '/' + url

    # Remove anchors.
    if '#' in url:
        url = url[:url.index('#')]

    parsed = urlparse(url)
    extension = os.path.splitext(parsed.path)[1]

    return url, parsed, extension


def valid_url(parsed_url, top_domain):
    """
    Validate if a given URL should be further crawled.
    'top_domain' is the netloc of the seed domain.
    """
    # Ignore irrelevant links.
    if parsed_url.scheme in ('mailto', 'tel', 'javascript'):
        return False

    # Check if link is outside domain.
    if parsed_url.netloc != top_domain:
        return False

    extension = os.path.splitext(parsed_url.path)[1]
    # Ignore predefined extensions.
    if extension in avoided_extensions:
        return False

    return True

