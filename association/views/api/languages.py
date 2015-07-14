from app.functions.piwik import track
from association.models import Language
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def list(request):
    """Handels a POST or GET request to list all languages.
    """
    track(request, 'list | languages | API | TIMA')
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'languages': [{
            'name':language.name,
            'code':language.code} for language in Language.objects.all()]}
    return HttpResponse(dumps(data), 'application/json')
