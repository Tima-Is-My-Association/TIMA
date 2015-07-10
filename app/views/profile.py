from app.forms import NewsletterForm, UserChangeForm
from app.functions.piwik import track
from app.models import AssociationHistory, Newsletter, Profile
from association.models import Language, Word
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _, ungettext
from django.views.decorators.csrf import csrf_protect

@login_required(login_url='/signin/')
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    track(request, 'Profile | TIMA')
    return render(request, 'tima/profile/profile.html', locals())

@login_required(login_url='/signin/')
def association_history(request):
    word = request.GET.get('word')
    l = request.GET.get('l')
    association_histories_list = AssociationHistory.objects.filter(user=request.user).order_by('-updated_at')
    if word:
        word = int(word)
        association_histories_list = association_histories_list.filter(Q(association__word__id=word) | Q(association__association__id=word))
    if l:
        association_histories_list = association_histories_list.filter(association__word__language__code=l)

    paginator = Paginator(association_histories_list, 50)
    page = request.GET.get('page')
    try:
        association_histories = paginator.page(page)
    except PageNotAnInteger:
        association_histories = paginator.page(1)
    except EmptyPage:
        association_histories = paginator.page(paginator.num_pages)

    track(request, 'Association history | Profile | TIMA')
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
            messages.success(request, _('Your profile has been successfully updated.'))
    else:
        profile = get_object_or_404(Profile, user=request.user)
        form = UserChangeForm(instance=request.user, initial={'cultural_background': profile.cultural_background})

    track(request, 'edit | Profile | TIMA')
    return render(request, 'tima/profile/form.html', locals())

@login_required(login_url='/signin/')
@csrf_protect
def newsletter(request):
    remove = request.GET.get('remove')

    languages = Language.objects.all()
    newsletter, created = Newsletter.objects.get_or_create(user=request.user)
    if not newsletter.user.email:
        messages.error(request, _('Without specifying an email-address, you can not receive a newsletter.'))

    if remove:
        newsletter.words.remove(get_object_or_404(Word, id=remove))
        newsletter.save()
        messages.success(request, _('You removed %(word)s successfully from your newsletter.') % {'word': get_object_or_404(Word, id=remove)})

    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            for word in form.cleaned_data['words']:
                newsletter.words.add(word)
            newsletter.save()
            messages.success(request, ungettext('Added %(words)s to your newsletter.', 'Added %(words)s to your newsletter.', len(form.cleaned_data['words'])) % {'words': ', '.join(['%s (%s)' % (word, word.language) for word in form.cleaned_data['words']])})
            form = NewsletterForm()
    else:
        form = NewsletterForm()

    track(request, 'Newsletter | Profile | TIMA')
    return render(request, 'tima/profile/newsletter.html', locals())
