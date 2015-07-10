from app.functions.piwik import track
from app.models import Newsletter
from association.models import Language, Word
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

def words(request):
    o = request.GET.get('o') if 'o' in request.GET else 'name'
    l = request.GET.get('l')
    r = request.GET.get('r')
    a = request.GET.get('a')
    search = request.GET.get('search')

    if request.user.is_authenticated():
        newsletter, created = Newsletter.objects.get_or_create(user=request.user)
        if r:
            newsletter.words.remove(get_object_or_404(Word, id=r))
            newsletter.save()
            messages.success(request, _('You removed %(word)s successfully from your newsletter.') % {'word': get_object_or_404(Word, id=r)})
        if a:
            newsletter.words.add(get_object_or_404(Word, id=a))
            newsletter.save()
            messages.success(request, _('You added %(word)s successfully to your newsletter.') % {'word': get_object_or_404(Word, id=a)})

    word_list = Word.objects.all().annotate(c=Count('word', distinct=True),
            a=Count('association', distinct=True)).order_by(Lower(o) if o == 'name' else o, Lower('name'))
    if l:
        lang = get_object_or_404(Language, code=l)
        word_list = word_list.filter(language=lang)
    if search:
        word_list = word_list.filter(name__icontains=search)

    paginator = Paginator(word_list, 100)
    page = request.GET.get('page')
    try:
        words = paginator.page(page)
        prange = paginator.page_range[max(int(page) - 4, 0):min(int(page) + 3, paginator.num_pages)]
        print(prange)
    except PageNotAnInteger:
        words = paginator.page(1)
        prange = [1, 2, 3, 4]
    except EmptyPage:
        words = paginator.page(paginator.num_pages)
        prange = [paginator.num_pages - 3, paginator.num_pages - 2, paginator.num_pages - 1, paginator.num_pages]

    track(request, 'Words | TIMA')
    return render(request, 'tima/words/words.html', locals())

def word(request, word_id):
    word = get_object_or_404(Word, id=word_id)
    track(request, '%s | TIMA' % word)
    return render(request, 'tima/words/word.html', locals())
