from app.functions.piwik import track
from app.models import Profile
from django.http import HttpResponse
from django.utils import timezone
from json import dumps

def leaderboard(request):
    """Handels GET/POST request to export the leaderboard.
    """
    track(request, 'leaderboard | API | TIMA')
    profiles = Profile.objects.all().order_by('-points')
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'leaderboard': [{'citizen_scientist':profile.user.username,
                    'points': profile.points,
                    'languages': [language.code for language in profile.languages.all()],
                    'cultural_background': profile.cultural_background}
                for profile in profiles]}
    return HttpResponse(dumps(data), 'application/json')
