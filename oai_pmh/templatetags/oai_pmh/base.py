from oai_pmh.templatetags.oai_pmh import register
from datetime import datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from oai_pmh.models import MetadataFormat, ResumptionToken, Set
from os import urandom

@register.simple_tag
def list_request_params(request):
    params = request.POST if request.method == 'POST' else request.GET
    return ' '.join(['%s="%s"' % (param, params.get(param)) for param in params])

@register.simple_tag
def timestamp(format_string):
    if format_string == 'UTC':
        return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    return timezone.now().strftime(format_string)

@register.simple_tag
def baseurl():
    return '%s%s' % (settings.ALLOWED_HOSTS[0], reverse('oai2'))

@register.simple_tag
def admin_emails():
    return '\n'.join(['<adminEmail>%s</adminEmail>' % admin[1] for admin in settings.ADMINS])

@register.simple_tag
def resumption_token(paginator, page, metadata_prefix=None, set_spec=None, from_timestamp=None, until_timestamp=None):
    if paginator.num_pages > 0 and page.has_next():
        expiration_date = datetime.utcnow() + timedelta(days=1)
        token = ''.join('%02x' % i for i in urandom(16))

        metadata_format = MetadataFormat.objects.get(prefix=metadata_prefix) if metadata_prefix else None
        set_spec = Set.objects.get(spec=set_spec) if set_spec else None

        ResumptionToken.objects.create(token=token, expiration_date=expiration_date, complete_list_size=paginator.count, cursor=page.end_index(), metadata_prefix=metadata_format, set_spec=set_spec, from_timestamp=from_timestamp, until_timestamp=until_timestamp)
        return '<resumptionToken expirationDate="%s" completeListSize="%s" cursor="%s">%s</resumptionToken>' % (expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ'), paginator.count, page.end_index(), token)
    else:
        return ''
