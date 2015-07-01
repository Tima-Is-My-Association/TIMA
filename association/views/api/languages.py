from app.functions.piwik import track
from association.models import Language
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def list(request):
    """Handels a POST or GET request to list all languages.
    """
    track(request, 'list | languages | API | TIMA')
    if request.method == 'POST' or request.method == 'GET':
        languages = Language.objects.all()

        data = {'languages': [{'name':language.name, 'code':language.code} for language in languages]}
        mimetype = 'application/json'

        return HttpResponse(dumps(data), mimetype)
    else:
         return HttpResponseBadRequest()
