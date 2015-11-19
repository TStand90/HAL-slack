import urllib.request
import urllib.parse
import json


def get_quote_of_the_day():
    qotdUrl = "http://quotesondesign.com/api/3.0/api-3.0.json"

    req = urllib.request.Request(qotdUrl)
    with urllib.request.urlopen(req) as response:
        downloadedPage = response.read()

    pageJson = json.loads(downloadedPage.decode('utf-8'))

    quote = pageJson.get('quote')
    author = pageJson.get('author')

    return ('"%s"\n- %s' % (quote, author))
