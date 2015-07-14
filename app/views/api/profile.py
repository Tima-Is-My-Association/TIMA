from app.functions.piwik import track
from app.models import AssociationHistory
from applications.models import AuthedUser
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from json import dumps

@csrf_exempt
def associationhistory(request):
    """Handels GET/POST request to export the leaderboard.
    """
    track(request, 'associationhistory | profile | API | TIMA')
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    autheduser = check_authed_user(params)
    if isinstance(autheduser, HttpResponse):
        return autheduser

    association_histories = AssociationHistory.objects.filter(user=autheduser.user)
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'association_history':[{'association':association_history.association, 'points':association_history.points} for association_history in association_histories]}
    return HttpResponse(dumps(data), 'application/json')
