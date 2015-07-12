from app.functions.piwik import track
from app.models import Profile
from association.models import Language
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def statistics(request):
    languages = Language.objects.all();
    user_count = Profile.objects.all().count()
    track(request, 'Statistics | TIMA')
    return render(request, 'tima/app/statistics.html', locals())
