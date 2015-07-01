from association.models import Word
from django.db.models import Count
from random import randint

def get_next_word(language, user=None, excludes=[]):
    """Returns the next word that should be asked for association.

    Keyword arguments:
    language --- language of the word
    user --- user object (default None)
    excludes --- list of words that should be exclude from the result (default [])
    """
    words = Word.objects.filter(languages=language)
    for exclude in excludes:
        words = words.exclude(id=exclude.id)

    if user and not user.is_anonymous():
        words = words.extra(select={'associationhistory_count': 'SELECT COUNT(*) FROM app_associationhistory JOIN association_association ON association_association.id=app_associationhistory.association_id WHERE association_association.word_id=association_word.id AND user_id=%s'}, select_params=[user.id]).order_by('associationhistory_count')[:15]
    else:
        words = words.order_by('count')[:15]
    return words[randint(0, (14 if words.count() == 15 else (words.count() - 1)))]

def build_graph(word, depth=2):
    nodes = []
    links = []
    n = {}
    n[word.id] = len(nodes)
    nodes.append({'id':word.id, 'name':word.name, 'group':0})
    _build_graph_rec(word, n, nodes, links, depth - 1)
    return (nodes, links)

def _build_graph_rec(word, n, nodes, links, depth):
    for a in word.word.all():
        if not a.association.id in n.keys():
            n[a.association.id] = len(nodes)
            nodes.append({'id':a.association.id,
                'name':a.association.name,
                'group':a.count})
        links.append({'source':n[word.id],
            'target':n[a.association.id],
            'value':a.count})

        if depth == 0:
            continue;

        for b in a.association.word.all():
            if not b.association.id in n:
                n[b.association.id] = len(nodes)
                nodes.append({'id':b.association.id,
                    'name':b.association.name,
                    'group':b.count})
            links.append({'source':n[a.association.id],
                'target':n[b.association.id],
                'value':b.count})
            if depth > 1:
                _build_graph_rec(b.association, n, nodes, links, depth - 2)