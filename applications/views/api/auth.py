from app.functions.piwik import track
from applications.functions.auth import check_authed_user
from applications.models import Application, AuthedUser, AuthRequest
from datetime import datetime
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
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
        try:
            user = get_user_model().objects.get(username=params.pop('username')[-1])
        except get_user_model().DoesNotExist:
            return HttpResponseNotFound('User with "username" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "username" is missing.')

    application = None
    if 'client_id' in params:
        try:
            application = Application.objects.get(client_id=params.pop('client_id')[-1])
        except Application.DoesNotExist:
            return HttpResponseNotFound('Apllication with "client_id" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "client_id" is missing.')

    authrequest, created = AuthRequest.objects.update_or_create(user=user, defaults={'timestamp':timezone.now()})
    data = {'timestamp': authrequest.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%f%z')}
    return HttpResponse(dumps(data), 'application/json')

@csrf_exempt
def user(request):
    """Handels a POST/GET request to auth a user.

    GET/POST parameters:
    username --- username
    password --- password
    timestamp --- timestamp send by auth/request request
    client_id --- client_id of the application
    token --- hash of application secret and n
    """
    track(request, 'user | auth | applications | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    user = None
    if 'username' in params and 'password' in params:
        user = authenticate(username=params.pop('username')[-1], password=params.pop('password')[-1])
        if not user or not user.is_active:
            return HttpResponseForbidden('User authentication fail or user is deactivated.')
    else:
        return HttpResponseBadRequest('Required parameter "username" or "password" are missing.')

    application = None
    if 'client_id' in params:
        try:
            application = Application.objects.get(client_id=params.pop('client_id')[-1])
        except Application.DoesNotExist:
            return HttpResponseNotFound('Application with "client_id" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "client_id" is missing.')

    authrequest = None
    if 'timestamp' in params and user:
        try:
            timestamp = datetime.strptime(params.pop('timestamp')[-1], '%Y-%m-%dT%H:%M:%S:%f%z')
            try:
                authrequest = AuthRequest.objects.get(user=user, timestamp=timestamp)
            except AuthRequest.DoesNotExist:
                return HttpResponseNotFound('AuthRequest with "timestamp" not found.')
        except Exception as e:
            return HttpResponseBadRequest('Required parameter "timestamp" has wrong format.')
    else:
        return HttpResponseBadRequest('Required parameter "timestamp" is missing.')

    if 'token' in params and application and authrequest:
        if sha512(('%s%s' % (application.secret, authrequest.timestamp.strftime('%Y-%m-%dT%H:%M:%S:%f%z'))).encode('utf-8')).hexdigest() != params.pop('token')[-1]:
            return HttpResponseForbidden('Wrong "token" given.')
    else:
        return HttpResponseBadRequest('Required parameter "token" is missing.')

    autheduser, created = AuthedUser.objects.update_or_create(user=user)
    authrequest.delete()
    data = {'n':autheduser.n, 'u':user.id, 'token':autheduser.token}
    return HttpResponse(dumps(data), 'application/json')

@csrf_exempt
def revoke(request):
    """Handels a POST/GET request to auth a user.

    GET/POST parameters:
    u --- int
    token --- hash of user token and n
    """
    track(request, 'revoke | auth | applications | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()
    autheduser = check_authed_user(params)
    if isinstance(autheduser, HttpResponse):
        return autheduser
    else:
        autheduser.delete()
        return HttpResponse(dumps({'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z')}), 'application/json')
