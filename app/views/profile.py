from app.models import AssociationHistory, Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

@login_required(login_url='/signin/')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'tima/profile/profile.html', locals())

@login_required(login_url='/signin/')
def association_history(request):
    association_histories_list = AssociationHistory.objects.filter(user=request.user).order_by('-updated_at')

    paginator = Paginator(association_histories_list, 50)
    page = request.GET.get('page')
    try:
        association_histories = paginator.page(page)
    except PageNotAnInteger:
        association_histories = paginator.page(1)
    except EmptyPage:
        association_histories = paginator.page(paginator.num_pages)

    return render(request, 'tima/profile/association_history.html', locals())