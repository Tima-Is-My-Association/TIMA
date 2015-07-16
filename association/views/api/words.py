from app.functions.piwik import track
from association.functions.wiktionary import exists
from association.functions.words import build_graph, get_next_word
from association.models import Language, Word
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

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
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'),
            'words': [word.to_json(request, limit=params.get('limit')) for word in words]}
    return HttpResponse(dumps(data), 'application/json')

@csrf_exempt
def graph(request):
    """Handels GET/POST request to get graph data for the given word.

    GET/POST parameters:
    word --- word
    language --- language of the word
    depth --- depth of associations (defailt 2)
    """
    track(request, 'graph | words | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    word = None
    if 'word' in params and 'language' in params:
        try:
            word = Word.objects.get(name=params.pop('word')[-1], language__code=params.pop('language')[-1])
        except Word.DoesNotExist:
            return HttpResponseNotFound('Word with "word" and "language" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "language" or "word" is missing.')

    depth = 2
    if 'depth' in params:
        depth = int(params.pop('depth')[-1])

    nodes, links = build_graph(word, depth)
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'), 'nodes':nodes, 'links':links}
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

    language = None
    if 'language' in params and 'word' in params:
        l = params.pop('language')[-1]
        try:
            language = Language.objects.get(code=l)
        except Language.DoesNotExist:
            return HttpResponseNotFound('Language with "%s" not found.' % l)

        w = params.pop('word')[-1]
        try:
            word = Word.objects.get(name=w, language=language)
        except Word.DoesNotExist:
            if not exists(language.code.lower(), w):
                return HttpResponseNotFound('Word with "%s" not found.' % w)
    else:
        return HttpResponseBadRequest('Required parameter "language" or "word" is missing.')
    return HttpResponse()

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

    language = None
    if 'language' in params:
        try:
            language = Language.objects.get(code=params.pop('language')[-1])
        except Language.DoesNotExist:
            return HttpResponseNotFound('Language with "language" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "language" is missing.')

    user = None
    if 'username' in params:
        try:
            user = get_user_model().objects.get(username=params.pop('username')[-1])
        except get_user_model().DoesNotExist:
            return HttpResponseNotFound('User with "username" not found.')
    excludes = []
    if 'excludes' in params:
        excludes = Word.objects.filter(name__in=params.pop('excludes'))

    word = get_next_word(language, user, excludes)
    data = {'word': word.name}
    return HttpResponse(dumps(data), 'application/json')
