from app.functions.piwik import track
from applications.models import Application, AuthedUser, AuthRequest
from datetime import datetime
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from hashlib import sha512
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
        application = get_object_or_404(Application, client_id=params.pop('client_id')[-1])
    else:
        return HttpResponseBadRequest()

    authrequest, created = AuthRequest.objects.update_or_create(user=user, defaults={'timestamp':timezone.now()})
    data = {'n': authrequest.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%fZ')}
    return HttpResponse(dumps(data), 'application/json')

@csrf_exempt
def user(request):
    """Handels a POST/GET request to auth a user.

    GET/POST parameters:
    username --- username
    password --- password
    n --- timestamp send by auth/request request
    client_id --- client_id of the application
    hash --- hash of application secret and n
    """
    track(request, 'request | auth | applications | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    user = None
    if 'username' in params and 'password' in params:
        user = authenticate(username=params.pop('username')[-1], password=params.pop('password')[-1])
        if not user or not user.is_active:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
    application = None
    if 'client_id' in params:
        application = get_object_or_404(Application, client_id=params.pop('client_id')[-1])
    else:
        return HttpResponseBadRequest()
    authrequest = None
    if 'n' in params and user:
        d = datetime.strptime(params.pop('n')[-1] + ' +0000', '%Y-%m-%dT%H:%M:%S:%fZ %z')
        authrequest = get_object_or_404(AuthRequest, user=user, timestamp=d)
    else:
        return HttpResponseBadRequest

    if 'hash' in params and application and authrequest:
        if sha512(('%s%s' % (application.secret, authrequest.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%fZ'))).encode('utf-8')).hexdigest() != params.pop('hash')[-1]:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest

    autheduser, created = AuthedUser.objects.update_or_create(user=user)
    authrequest.delete()
    data = {'n':autheduser.n, 'token':autheduser.token}
    return HttpResponse(dumps(data), 'application/json')
