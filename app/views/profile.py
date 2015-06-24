from app.forms import UserChangeForm
from app.functions.piwik import track
from app.models import AssociationHistory, Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

@login_required(login_url='/signin/')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    track(request, 'Profile | TIMA')
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

    track(request, 'Association history | TIMA')
    return render(request, 'tima/profile/association_history.html', locals())

@login_required(login_url='/signin/')
@csrf_protect
def edit(request):
    if request.method == 'POST':
        form = UserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()

            if form.cleaned_data['cultural_background']:
                profile = get_object_or_404(Profile, user=user)
                profile.cultural_background = form.cleaned_data['cultural_background']
                profile.save()
            print(form.cleaned_data['cultural_background'])
            messages.success(request, 'Your profile has been successfully updated.')
    else:
        form = UserChangeForm(instance=request.user)

    track(request, 'edit | TIMA')
    return render(request, 'tima/profile/form.html', locals())