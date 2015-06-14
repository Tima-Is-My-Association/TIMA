from association.functions.words import get_next_word
from association.models import Association, Language, Word
from django.shortcuts import get_object_or_404, render
from association.forms import AssociationForm

def home(request):
    languages = Language.objects.all()
    return render(request, 'tima/association/home.html', locals())

def association(request, slug):
    language = get_object_or_404(Language, slug=slug)

    if request.method == 'POST':
        form = AssociationForm(request.POST)
        if form.is_valid():
            word, created = Word.objects.get_or_create(name=form.cleaned_data['word'])
            if created:
                word.languages.add(language)
                word.save()
            association, created = Word.objects.get_or_create(name=form.cleaned_data['association'])
            if created:
                word.languages.add(language)
                word.save()

            association, created = Association.objects.update_or_create(word=word, association=association)
        else:
            word = Word.objects.get(name=form.cleaned_data['word'])
            return render(request, 'tima/association/association.html', locals())

    word = get_next_word(language=language)
    form = AssociationForm(initial={'word':word.name})
    return render(request, 'tima/association/association.html', locals())