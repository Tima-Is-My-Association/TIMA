from app.templatetags.tima import register
from django.template.loader import get_template

@register.simple_tag(takes_context=True)
def bootstrap_messages(context, *args, **kwargs):
    return get_template('bootstrap/messages.html').render(context)