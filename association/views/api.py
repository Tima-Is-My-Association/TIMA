from association.models import Word
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from json import dumps

def graph(request, word_id):
    word = get_object_or_404(Word, id=word_id)

    nodes = []
    links = []
    n = {}
    n[word.id] = len(nodes)
    nodes.append({'id':word.id, 'name':word.name, 'group':0})
    for a in word.word.all():
        if not a.association.id in n:
            n[a.association.id] = len(nodes)
            nodes.append({'id':a.association.id, 'name':a.association.name, 'group':a.count})
        links.append({'source':n[word.id], 'target':n[a.association.id], 'value':a.count})
        for b in a.association.word.all():
            if not b.association.id in n:
                n[b.association.id] = len(nodes)
                nodes.append({'id':b.association.id, 'name':b.association.name, 'group':b.count})
            links.append({'source':n[a.association.id], 'target':n[b.association.id], 'value':b.count})

    data = {'nodes':nodes, 'links':links}

    mimetype = 'application/json'
    return HttpResponse(dumps(data), mimetype)