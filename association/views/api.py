from association.models import Word
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from json import dumps

def graph(request, word_id):
    word = get_object_or_404(Word, id=word_id)

    nodes = []
    links = []
    nodes.append({'id':word.id, 'name':word.name, 'group':0})
    for association in word.word.all():
        nodes.append({'id':association.association.id, 'name':association.association.name, 'group':association.count})
        links.append({'source':0, 'target':len(nodes) - 1, 'value':association.count})
    data = {'nodes':nodes, 'links':links}

    mimetype = 'application/json'
    return HttpResponse(dumps(data), mimetype)