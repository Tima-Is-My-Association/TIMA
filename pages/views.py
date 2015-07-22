from app.functions.piwik import track
from django.shortcuts import get_object_or_404, render
from pages.models import Page

def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    track(request, '%s | TIMA' % page.title)
    return render(request, 'tima/pages/page.html', locals())

def faq(request):
    track(request, 'FAQ | TIMA')
    return render(request, 'tima/pages/faq.html', locals())
