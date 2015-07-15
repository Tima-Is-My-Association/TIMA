# -*- coding: utf-8 -*-

from json import loads
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

def fetch(language, word, limit=1):
    """Makes a GET request to wiktionary and search for the given word and return the json result.

    Keyword arguments:
    language --- language of the word
    word --- word to check
    limit --- limits the number of results (default 1)
    """
    with urlopen('https://%s.wiktionary.org/w/api.php?action=opensearch&search=%s&limit=%s' % (language, quote(word), limit)) as response:
        data = response.read().decode('utf-8')
    response.close()
    return loads(data)

def exists(language, word):
    """Checks the Wiktionary if the given word exists and returns True or False.

    Keyword arguments:
    language --- language of the word
    word --- word to check
    """
    try:
        return len(fetch(language, word)[1]) == 1
    except HTTPError:
        return False
