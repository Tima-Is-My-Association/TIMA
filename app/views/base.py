from app.forms import UserCreationForm
from app.functions.piwik import track
from app.models import Profile
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, views
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signin(request):
    gnext = request.GET.get('next')
    track(request, 'Sign in | TIMA')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'You have successfully logged in.')

                try:
                    Profile.objects.get(user=user)
                except Profile.DoesNotExist:
                    Profile.objects.create(user=user)

                return redirect(gnext) if gnext else redirect('home')
            else:
                messages.add_message(request, messages.ERROR, 'Your account is disabled.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.add_message(request, messages.ERROR, 'Please enter a correct username and password to log in. Note that both fields may be case-sensitive.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = AuthenticationForm(request)
        return render(request, 'registration/login.html', locals())

@csrf_protect
def signup(request):
    track(request, 'Sign up | TIMA')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
            messages.info(request, 'Thanks for signing up. You are now logged in.')
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            return redirect(reverse('profile'))
        else:
            return render(request, 'registration/signup.html', locals())
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', locals())

@csrf_protect
def password_reset_confirm(request, uidb64=None, token=None):
    return views.password_reset_confirm(request, uidb64=uidb64, token=token, post_reset_redirect=reverse('signin'))

@csrf_protect
def password_reset(request):
    return views.password_reset(request, post_reset_redirect=reverse('signin'))
