from app.functions.score import calculate_points
from association.forms import AssociationForm
from association.functions.words import get_next_word
from association.models import Association, Language, Word
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect

def home(request):
    languages = Language.objects.all()
    return render(request, 'tima/association/home.html', locals())

@csrf_protect
def association(request, slug):
    language = get_object_or_404(Language, slug=slug)

    excludes = []
    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            word, created = Word.objects.get_or_create(name=form.cleaned_data['word'])
            if created:
                word.languages.add(language)
                word.save()
            word1, created = Word.objects.get_or_create(name=form.cleaned_data['association'])
            if created:
                word1.languages.add(language)
                word1.save()

            association, created = Association.objects.update_or_create(word=word, association=word1)
            excludes.append(word)
            excludes.append(word1)
            if not request.user.is_anonymous():
                points = calculate_points(request.user, association)
                messages.add_message(request, messages.INFO, 'You received %s points for your association of %s.' % (points, association))
        else:
            word = Word.objects.get(name=form.cleaned_data['word'])
            return render(request, 'tima/association/association.html', locals())

    word = get_next_word(language=language, user=request.user, excludes=excludes)
    form = AssociationForm(initial={'word':word.name})
    return render(request, 'tima/association/association.html', locals())