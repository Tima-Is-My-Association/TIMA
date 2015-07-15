from applications.models import AuthedUser
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from hashlib import sha512

def check_authed_user(params):
    if 'u' in params and 'token' in params:
        try:
            autheduser = AuthedUser.objects.get(user__id=params.pop('u')[-1])
            if sha512(('%s%s' % (autheduser.token, autheduser.n + 1)).encode('utf-8')).hexdigest() != params.pop('token')[-1]:
                return HttpResponseForbidden('Wrong "token" given.')
            return autheduser
        except AuthedUser.DoesNotExist:
            return HttpResponseNotFound('AuthedUser with "u" not found.')
    else:
        return HttpResponseBadRequest('Required parameter "u" or "token" is missing.')
