from oai_pmh.templatetags.oai_pmh import register
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone
from html import escape
from oai_pmh.models import MetadataFormat, ResumptionToken, Set
from os import urandom

@register.simple_tag
def list_request_attributes(verb=None, identifier=None, metadata_prefix=None, from_timestamp=None, until_timestamp=None, set_spec=None, resumption_token=None):
    attributes = ('verb="%s"' % verb) if verb and verb in ['Identify', 'ListMetadataFormats', 'ListSets', 'GetRecord', 'ListIdentifiers', 'ListRecords'] else ''
    attributes += (' identifier="%s"' % escape(identifier)) if identifier else ''
    attributes += (' metadataPrefix="%s"' % escape(metadata_prefix)) if metadata_prefix else ''
    attributes += (' from="%s"' % from_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')) if from_timestamp else ''
    attributes += (' until="%s"' % until_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')) if until_timestamp else ''
    attributes += (' set="%s"' % escape(set_spec)) if set_spec else ''
    attributes += (' resumptionToken="%s"' % escape(resumption_token)) if resumption_token else ''
    return attributes

@register.simple_tag
def timestamp(format_string):
    if format_string == 'UTC':
        return timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
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
        expiration_date = timezone.now() + timezone.timedelta(days=1)
        token = ''.join('%02x' % i for i in urandom(16))

        metadata_format = MetadataFormat.objects.get(prefix=metadata_prefix) if metadata_prefix else None
        set_spec = Set.objects.get(spec=set_spec) if set_spec else None

        ResumptionToken.objects.create(token=token, expiration_date=expiration_date, complete_list_size=paginator.count, cursor=page.end_index(), metadata_prefix=metadata_format, set_spec=set_spec, from_timestamp=from_timestamp, until_timestamp=until_timestamp)
        return '<resumptionToken expirationDate="%s" completeListSize="%s" cursor="%s">%s</resumptionToken>' % (expiration_date.strftime('%Y-%m-%dT%H:%M:%SZ'), paginator.count, page.end_index(), token)
    else:
        return ''

@register.simple_tag
def multiple_tags(string, tag, delimiter=';'):
    return '\n'.join(['<%s>%s</%s>' % (tag, s, tag) for s in string.split(delimiter)])
