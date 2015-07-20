from app.functions.piwik import track
from app.models import AssociationHistory, Profile
from applications.functions.auth import check_authed_user
from applications.models import AuthedUser
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def associationhistory(request):
    """Handels GET/POST request to export the association history of the authed user.

    GET/POST parameters:
    u --- int
    token --- hash of user token and n
    """
    track(request, 'associationhistory | profile | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    autheduser = check_authed_user(params)
    if isinstance(autheduser, HttpResponse):
        return autheduser

    association_histories = AssociationHistory.objects.filter(user=autheduser.user)
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'),
        'association_history':[{'association':association_history.association.to_json(request), 'points':association_history.points} for association_history in association_histories]}
    return HttpResponse(dumps(data), 'application/json')

@csrf_exempt
def profile(request):
    """Handels GET/POST request to export a profile of the authed user.

    GET/POST parameters:
    u --- int
    token --- hash of user token and n
    """
    track(request, 'profile | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    autheduser = check_authed_user(params)
    if isinstance(autheduser, HttpResponse):
        return autheduser

    profile = Profile.objects.get(user=autheduser.user)
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%S:%f%z'),
                'profile':{'username':profile.user.username,
                            'points':profile.points,
                            'cultural_background': profile.cultural_background,
                            'first_name': profile.user.first_name,
                            'last_name': profile.user.last_name,
                            'email': profile.user.email,}}
    return HttpResponse(dumps(data), 'application/json')
