from association.models import Word
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render

def words(request):
    word_list = Word.objects.all()

    paginator = Paginator(word_list, 50)
    page = request.GET.get('page')
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    return render(request, 'tima/words/words.html', locals())

def word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    return render(request, 'tima/words/word.html', locals())