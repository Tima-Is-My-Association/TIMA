# -*- coding: utf-8 -*-

from json import loads
from urllib.parse import quote
from urllib.request import urlopen

def fetch(language, word, limit=1):
    with urlopen('https://%s.wiktionary.org/w/api.php?action=opensearch&search=%s&limit=%s' % (language, quote(word), limit)) as response:
        data = response.read().decode('utf-8')
    response.close()
    return loads(data)

def exists(language, word):
    return len(fetch(language, word)[1]) == 1
