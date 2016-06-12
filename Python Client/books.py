import os
import requests

base_url = 'http://test123.podzone.net'

def fetch(book_url, force=False):
    # typical book_url is '/book_json/1'
    bookNumber = book_url[book_url.rfind('/')+1:]
    jsonPath = 'cache/book' + bookNumber + '.json'
    if force or (not os.path.isfile(jsonPath)):
        # fetch the file only if not already in cache
        url = base_url + book_url
        r = requests.get(url, stream=True)
        with open(jsonPath, 'wb') as fd:
            for chunk in r.iter_content(1024):
                fd.write(chunk)
    return jsonPath
