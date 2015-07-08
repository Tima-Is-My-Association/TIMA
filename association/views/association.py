from app.functions.piwik import track
from app.functions.score import calculate_points
from app.models import Profile
from association.forms import AssociationForm
from association.functions.words import get_next_word
from association.models import Association, Language, Word
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _

def home(request):
    languages = Language.objects.all()
    track(request, 'TIMA')
    return render(request, 'tima/association/home.html', locals())

@csrf_protect
def association(request, slug):
    language = get_object_or_404(Language, slug=slug)

    if not request.user.is_anonymous():
        language.users.add(get_object_or_404(Profile, user=request.user))
        language.save()

    excludes = []
    if 'excludes' in request.GET:
        for exclude in request.GET.getlist('excludes'):
            excludes.append(get_object_or_404(Word, name=exclude, language=language))

    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['word'] == form.cleaned_data['association']:
                word = Word.objects.get(name=form.cleaned_data['word'], language=language)
                return render(request, 'tima/association/association.html', locals())

            word = get_object_or_404(Word, name=form.cleaned_data['word'], language=language)
            word1, created = Word.objects.get_or_create(name=form.cleaned_data['association'], language=language)

            association, created = Association.objects.update_or_create(word=word, association=word1)
            excludes.append(word)
            excludes.append(word1)
            points = calculate_points(request.user if not request.user.is_anonymous() else None, association)
            if not request.user.is_anonymous():
                messages.add_message(request, messages.INFO, _('You received %(points)s points for your association of %(association)s.') % {'points': points, 'association': association})
            else:
                messages.add_message(request, messages.INFO, _('Your association %(association)s has been saved. If you had been signed in you would have received %(points)s points.') % {'association': association, 'points':points})
        else:
            word = Word.objects.get(name=form.cleaned_data['word'], language=language)
            association1 = form.cleaned_data['association1']
            return render(request, 'tima/association/association.html', locals())

    word = get_next_word(language=language, user=request.user, excludes=excludes)
    association1 = ''
    form = AssociationForm(initial={'word':word.name, 'language':language.code})
    track(request, 'Association | TIMA')
    return render(request, 'tima/association/association.html', locals())
