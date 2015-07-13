from app.functions.piwik import track
from applications.models import Application, AuthRequest
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def request(request):
    """Handels a POST/GET request to want to auth.

    GET/POST parameters:
    username --- username
    client_id --- client_id of the application
    """
    track(request, 'request | auth | applications | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    user = None
    if 'username' in params:
        user = get_object_or_404(get_user_model(), username=params.pop('username')[-1])
    else:
        return HttpResponseBadRequest()
    client_id = None
    if 'client_id' in params:
        client_id = get_object_or_404(Application, client_id=params.pop('client_id')[-1])
    else:
        return HttpResponseBadRequest()

    authrequest, created = AuthRequest.objects.update_or_create(user=user, defaults={'timestamp':timezone.now()})
    data = {'n': authrequest.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%fZ')}
    return HttpResponse(dumps(data), 'application/json')
