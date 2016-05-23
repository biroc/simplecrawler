import json


def output(url, links, assets):
    """
    Given a page, save it as a json in the sitemap file.
    """
    page = {'URL': url, 'Links': links, 'Assets': assets}
    formatted_json = json.dumps(page, indent=3, separators=(',', ': '))
    print(formatted_json)
