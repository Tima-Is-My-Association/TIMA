from oai_pmh.templatetags.oai_pmh import register
from datetime import datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from oai_pmh.models import ResumptionToken
from os import urandom

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

@register.simple_tag
def resumptionToken(paginator, page):
    if paginator.num_pages > 0 and page.has_next():
        expirationDate = datetime.utcnow() + timedelta(days=1)
        token = ''.join('%02x' % i for i in urandom(16))
        ResumptionToken.objects.create(token=token, expiration_date=expirationDate, complete_list_size=paginator.count, cursor=page.end_index())
        return '<resumptionToken expirationDate="%s" completeListSize="%s" cursor="%s">%s</resumptionToken>' % (expirationDate.strftime('%Y-%m-%dT%H:%M:%SZ'), paginator.count, page.end_index(), token)
    else:
        return ''
