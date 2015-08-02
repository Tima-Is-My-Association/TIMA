from app.functions.piwik import track
from app.models import ExcludeWord
from applications.functions.auth import check_authed_user
from association.models import Language, Word
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def add(request):
    """Handels GET/POST adds the given word to the list of exclude list of the user.

    GET/POST parameters:
    u --- int
    token --- hash of user token and n
    word --- word to add to exclude list
    language --- language of the word
    """
    track(request, 'add | excludeword | profile | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    autheduser = check_authed_user(params)
    if isinstance(autheduser, HttpResponse):
        return autheduser

    word = None
    if 'language' in params and 'word' in params:
        language_code = params.pop('language')[-1]
        try:
            language = Language.objects.get(code=language_code)
        except Language.DoesNotExist:
            return HttpResponseNotFound('Language with "%s" not found.' % language_code)

        word_name = params.pop('word')[-1]
        try:
            word = Word.objects.get(name=word_name, language=language)
        except Word.DoesNotExist:
            return HttpResponseNotFound('Word with "%s" not found.' % word_name)
    else:
        return HttpResponseBadRequest('Required parameter "language" or "word" is missing.')

    excludeword, created = ExcludeWord.objects.get_or_create(word=word, user=autheduser.user)
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'), 'created':created}
    return HttpResponse(dumps(data), 'application/json')
