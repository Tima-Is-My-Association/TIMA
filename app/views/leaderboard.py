from app.functions.piwik import track
from app.models import Profile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

def leaderboard(request):
    search = request.GET.get('search')
    profile_list = Profile.objects.extra(select={'rank':'RANK() OVER (ORDER BY points DESC)'}).all().order_by('rank')
    if search:
        profile_list = profile_list.filter(user__username__icontains=search)

    paginator = Paginator(profile_list, 50)
    page = request.GET.get('page')
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        if request.user.is_authenticated() and not search:
            profiles = paginator.page(min(Profile.objects.filter(points__gt=Profile.objects.get(user=request.user).points).count() / 3 + 1, paginator.num_pages))
        else:
            profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    track(request, 'Leaderboard | TIMA')
    return render(request, 'tima/app/leaderboard.html', locals())
