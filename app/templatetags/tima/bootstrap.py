from app.templatetags.tima import register
from django.template.loader import get_template

@register.simple_tag(takes_context=True)
def bootstrap_messages(context, *args, **kwargs):
    return get_template('bootstrap/messages.html').render(context)

@register.simple_tag(takes_context=True)
def pagination(context, paginator, page, *args, **kwargs):
    context['prange'] = paginator.page_range[max(int(page.number) - 4, 0):min(int(page.number) + 3, paginator.num_pages)]
    context['page'] = page
    context['kwargs'] = kwargs
    return get_template('bootstrap/pagination.html').render(context)
