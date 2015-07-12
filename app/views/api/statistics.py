from app.functions.piwik import track
from app.models import Profile
from association.models import Association, Language
from django.http import HttpResponse
from django.utils import timezone
from json import dumps

def statistics(request):
    """Handels GET/POST request to export statistics.
    """
    track(request, 'statistics | API | TIMA')
    languages = Language.objects.all();
    user_count = Profile.objects.all().count()
    data = {'response_date':timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'statistics': [{'citizen_scientists': user_count,
                    'languages': [{'language': language.code,
                        'words': language.words.count(),
                        'associations': Association.objects.filter(word__language=language).count()
                    } for language in languages]}]}
    return HttpResponse(dumps(data), 'application/json')
