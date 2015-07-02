from oai_pmh.templatetags.oai_pmh import register
from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse

@register.simple_tag
def timestamp(format_string):
    if format_string == 'UTC':
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    return datetime.now().strftime(format_string)

@register.simple_tag
def baseurl():
    return '%s%s' % (settings.ALLOWED_HOSTS[0], reverse('oai2'))

@register.simple_tag
def adminemails():
    return '\n'.join(['<adminEmail>%s</adminEmail>' % admin[1] for admin in settings.ADMINS])
