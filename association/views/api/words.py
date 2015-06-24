from association.functions.words import build_graph, get_next_word
from association.models import Language, Word
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def next(request):
    """Handels a POST request for the next word.

    POST parameters:
    language --- language of the word
    username --- username of a user
    excludes --- list of words that should be exclude from the result (optinal)
    """
    if request.method == 'POST':
        language = get_object_or_404(Language,
            code=request.POST.get('language'))

        user = None
        if 'username' in request.POST:
            user = get_object_or_404(get_user_model(),
                username=request.POST.get('username'))

        excludes = []
        if 'excludes' in request.POST:
            excludes = Word.objects.filter(name__in=
                request.POST.getlist('excludes'))

        word = get_next_word(language)
        data = {'word': word.name}
        mimetype = 'application/json'

        return HttpResponse(dumps(data), mimetype)
    else:
         return HttpResponseBadRequest()

def graph(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    depth = int(request.GET.get('depth')) if request.GET.get('depth') else 2

    nodes, links = build_graph(word, depth)
    data = {'nodes':nodes, 'links':links}

    mimetype = 'application/json'
    return HttpResponse(dumps(data), mimetype)