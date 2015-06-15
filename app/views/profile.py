from app.models import AssociationHistory, Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

@login_required(login_url='/signin/')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'tima/profile/profile.html', locals())

@login_required(login_url='/signin/')
def association_history(request):
    association_histories = AssociationHistory.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'tima/profile/association_history.html', locals())