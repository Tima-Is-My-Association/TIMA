from app.functions.piwik import track
from app.functions.score import calculate_points
from applications.functions.auth import check_authed_user
from applications.models import AuthedUser
from association.models import Association, Language, Word
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def association(request):
    """Handels a POST or GET request to save a association.

    GET/POST parameters:
    language --- language of the word and association
    word --- word
    association --- association
    u --- int
    token --- hash of user token and n
    """
    track(request, 'association | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    autheduser = check_authed_user(params)
    if isinstance(autheduser, HttpResponse):
        return autheduser

    language = None
    if 'language' in params:
        try:
            language = Language.objects.get(code=params.pop('language')[-1])
        except Language.DoesNotExist:
            return HttpResponseNotFound('Language with "language" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "language" is missing.')

    word = None
    if 'word' in params:
        try:
            word = Word.objects.get(name=params.pop('word')[-1], language=language)
        except Word.DoesNotExist:
            return HttpResponseNotFound('Word with "word" and "language" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "word" is missing.')

    word1 = None
    points = 0
    if 'association' in params:
        word1, created = Word.objects.get_or_create(name=params.pop('association')[-1], language=language)
        association, created = Association.objects.update_or_create(word=word, association=word1)
        points = calculate_points(autheduser.user, association)
    else:
        return HttpResponseBadRequest('Required parameter "association" is missing.')

    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'), 'points':points}
    return HttpResponse(dumps(data), 'application/json')
