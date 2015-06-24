from app.functions.piwik import track
from app.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def leaderboard(request):
    profile_list = Profile.objects.all().order_by('-points')

    paginator = Paginator(profile_list, 50)
    page = request.GET.get('page')
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    track(request, 'Leaderboard | TIMA')
    return render(request, 'tima/leaderboard/leaderboard.html', locals())