from app.functions.piwik import track
from association.functions.words import build_graph, get_next_word
from association.models import Language, Word
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def next(request):
    """Handels a POST/GET request for the next word.

    GET/POST parameters:
    language --- language of the word
    username --- username of a user (optinal)
    excludes --- list of words that should be exclude from the result (optinal)
    """

    language = None
    user = None
    excludes = []
    track(request, 'next | words | API | TIMA')
    if request.method == 'POST':
        language = get_object_or_404(Language,
            code=request.POST.get('language'))

        if 'username' in request.POST:
            user = get_object_or_404(get_user_model(),
                username=request.POST.get('username'))

        if 'excludes' in request.POST:
            excludes = Word.objects.filter(name__in=
                request.POST.getlist('excludes'))
    elif request.method == 'GET':
        language = get_object_or_404(Language,
            code=request.GET.get('language'))

        if 'username' in request.GET:
            user = get_object_or_404(get_user_model(),
                username=request.GET.get('username'))

        if 'excludes' in request.GET:
            excludes = Word.objects.filter(name__in=
                request.GET.getlist('excludes'))
    else:
         return HttpResponseBadRequest()

    word = get_next_word(language, user, excludes)
    data = {'word': word.name}
    mimetype = 'application/json'

    return HttpResponse(dumps(data), mimetype)

def graph(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    depth = int(request.GET.get('depth')) if request.GET.get('depth') else 2

    nodes, links = build_graph(word, depth)
    data = {'nodes':nodes, 'links':links}

    mimetype = 'application/json'
    track(request, 'graph | words | API | TIMA')
    return HttpResponse(dumps(data), mimetype)

def export(request, word_id=None):
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    if word_id:
        word = get_object_or_404(Word, id=word_id)
        data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'words': [word.to_json(request, limit=params.get('limit'))]}
    else:
        words = Word.objects.all().order_by(Lower('name'))
        if 'word' in params:
            words = words.filter(id__in=params.pop('word'))
        if 'language' in params:
            words = words.filter(language__code=params.pop('language')[-1])
        data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                'words': [word.to_json(request, limit=params.get('limit')) for word in words]}
    return HttpResponse(dumps(data), 'application/json')

@csrf_exempt
def isA(request):
    """Handels a GET/POST request to check if a given word is a word.

    GET/POST parameters:
    language --- language of the word
    word --- word to check
    """
    track(request, 'isA | words | API | TIMA')
    if request.method == 'POST':
        language = get_object_or_404(Language,
            code=request.POST.get('language'))
        word = get_object_or_404(Word,
            name=request.POST.get('word'), language=language)
        return HttpResponse()
    elif request.method == 'GET':
        language = get_object_or_404(Language,
            code=request.GET.get('language'))
        word = get_object_or_404(Word,
            name=request.GET.get('word'), language=language)
        return HttpResponse()
    else:
         return HttpResponseBadRequest()
