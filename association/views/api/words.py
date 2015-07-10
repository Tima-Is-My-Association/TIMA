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

    track(request, 'next | words | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    language = get_object_or_404(Language, code=params.pop('language')[-1])

    user = None
    if 'username' in params:
        user = get_object_or_404(get_user_model(),
                username=params.pop('username')[-1])
    excludes = []
    if 'excludes' in params:
        excludes = Word.objects.filter(name__in=params.pop('excludes'))

    word = get_next_word(language, user, excludes)
    data = {'word': word.name}
    return HttpResponse(dumps(data), 'application/json')

def graph(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    depth = int(request.GET.get('depth')) if request.GET.get('depth') else 2

    nodes, links = build_graph(word, depth)
    data = {'nodes':nodes, 'links':links}

    mimetype = 'application/json'
    track(request, 'graph | words | API | TIMA')
    return HttpResponse(dumps(data), mimetype)

def export(request):
    """Handels GET/POST request to export word(s) with their associations.

    GET/POST parameters:
    language --- language of the word(s) (optinal)
    word --- list of word ids to include (optinal)
    limit --- limit the number of associations per word (optinal)
    """
    track(request, 'words | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()
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
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    language = get_object_or_404(Language, code=params.pop('language')[-1])
    word = get_object_or_404(Word, name=params.pop('word')[-1], language=language)
    return HttpResponse()
