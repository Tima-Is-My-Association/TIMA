from app.models import Profile
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def ulogin(request):
    gnext = request.GET.get('next')
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