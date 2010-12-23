#!/usr/bin/python
# from http://dcortesi.com/2008/05/28/google-ajax-search-api-example-python-code/
from __future__ import with_statement
try:
    from urllib.parse import quote, urlencode
    from urllib.request import urlopen
except ImportError:
    from urllib import quote, urlencode, urlopen
from json import loads
from xgoogle.search import GoogleSearch
import re

def search(term, v='1.0'):
    query = urlencode({'q' : term})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=%s&%s' % (v, query)
    search_results = urlopen(url)
    json = loads(search_results.read())
    return json

reg = re.compile('<div id="resultStats">\\s*About ([0-9,]+) results')
def get_number_of_results(term, ajax=False, verbose=True):
    if not ajax:
        gs = GoogleSearch(term)
        page = str(gs._get_results_page())
        match = reg.search(page)
        if match:
            if verbose: print(term, match.groups()[0])
            return int(match.groups()[0].replace(',',''))
        else:
            raw_input((term, page))
    return int(search(term)['responseData']['cursor']['estimatedResultCount'])
        
##popularity = [(get_popularity(alphabet, True), alphabet) for alphabet in get_accepted_image_list()]
