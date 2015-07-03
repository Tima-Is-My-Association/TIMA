from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from oai_pmh.models import Header, MetadataFormat, Set, ResumptionToken

PER_PAGE = 1

@csrf_exempt
def oai2(request):
    """
    Handels all OAI-PMH v2 requets. For details see
    https://www.openarchives.org/OAI/openarchivesprotocol.html
    """
    global PER_PAGE

    errors = []
    from_timestamp = None
    until_timestamp = None
    params = request.POST.copy() if request.method == 'POST' else request.GET.copy()

    if 'verb' in params:
        verb = params.pop('verb')[-1]
        if verb == 'Identify':
            template = 'tima/oai_pmh/identify.xml'
            check_bad_arguments(params, errors)
        elif verb == 'ListIdentifiers':
            template = 'tima/oai_pmh/listidentifiers.xml'

            if 'resumptionToken' in params:
                header_list = Header.objects.all()
                paginator, headers = do_resumption_token(params, errors, header_list)
            elif 'metadataPrefix' in params:
                metadata_prefix = params.pop('metadataPrefix')[-1]
                if not MetadataFormat.objects.filter(prefix=metadata_prefix).exists():
                    errors.append({'code':'cannotDisseminateFormat', 'msg':'The value of the metadataPrefix argument "%s" is not supported.' % metadata_prefix})
                else:
                    header_list = Header.objects.filter(metadata_formats__prefix=metadata_prefix)

                    if 'set' in params:
                        if Set.objects.all().count() == 0:
                            errors.append({'code':'noSetHierarchy', 'msg':'This repository does not support sets.'})
                        else:
                            set_spec = params.pop('set')[-1]
                            header_list = header_list.filter(sets__spec=set_spec)
                    if 'from' in params:
                        from_timestamp = datetime.strptime(params.pop('from')[-1] + ' +0000', '%Y-%m-%dT%H:%M:%SZ %z')
                        header_list = header_list.filter(timestamp__gte=from_timestamp)
                    if 'until' in params:
                        until_timestamp = datetime.strptime(params.pop('until')[-1] + ' +0000', '%Y-%m-%dT%H:%M:%SZ %z')
                        header_list = header_list.filter(timestamp__lte=until_timestamp)

                    if header_list.count() == 0:
                        errors.append({'code':'noRecordsMatch', 'msg':'The combination of the values of the from, until, and set arguments results in an empty list.'})
                    else:
                        paginator = Paginator(header_list, PER_PAGE)
                        headers = paginator.page(1)
            else:
                errors.append({'code':'badArgument', 'msg':'The required argument "metadataPrefix" is missing in the request.'})
            check_bad_arguments(params, errors)
        elif verb == 'ListMetadataFormats':
            template = 'tima/oai_pmh/listmetadataformats.xml'
            metadataformats = MetadataFormat.objects.all()

            if 'identifier' in params:
                identifier = params.pop('identifier')[-1]
                if Header.objects.filter(identifier=identifier).exists():
                    metadataformats = metadataformats.filter(identifiers__identifier=identifier)
                else:
                    errors.append({'code':'idDoesNotExist', 'msg':'A record with the identifier "%s" does not exist.' % identifier})
            if metadataformats.count() == 0:
                errors.append({'code':'noMetadataFormats', 'msg':'There are no metadata formats available for the record with identifier "%s".' % identifier})
            check_bad_arguments(params, errors)
        elif verb == 'ListSets':
            template = 'tima/oai_pmh/listsets.xml'

            if not Set.objects.all().exists():
                errors.append({'code':'noSetHierarchy', 'msg':'This repository does not support sets.'})
            else:
                paginator, sets = do_resumption_token(params, errors, Set.objects.all())
            check_bad_arguments(params, errors)
        else:
            errors.append({'code':'badVerb', 'msg':'The verb "%s" provided in the request is illegal.' % verb})
    else:
        errors.append({'code':'badVerb', 'msg':'The request does not provide any verb.'})
    return render(request, template if not errors else 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')

def check_bad_arguments(params, errors, msg=None):
    for k,v in params.copy().items():
        errors.append({'code':'badArgument', 'msg':'The argument "%s" (value="%s") included in the request is not valid.%s' % (k, v, (' %s' % msg if msg else ''))})
        params.pop(k)

def do_resumption_token(params, errors, objs):
    if 'resumptionToken' in params:
        resumption_token = params.pop('resumptionToken')[-1]
        try:
            rt = ResumptionToken.objects.get(token=resumption_token)
            if timezone.now() > rt.expiration_date:
                errors.append({'code':'badResumptionToken', 'msg':'The resumptionToken "%s" is expired.' % resumption_token})
            else:
                if rt.set_spec:
                    objs = objs.filter(sets=rt.set_spec)
                if rt.metadata_prefix:
                    objs = objs.filter(metadata_formats=rt.metadata_prefix)
                if rt.from_timestamp:
                    objs = objs.filter(timestamp__gte=rt.from_timestamp)
                if rt.until_timestamp:
                    objs = objs.filter(timestamp__gte=rt.until_timestamp)

                paginator = Paginator(objs, PER_PAGE)
                try:
                    page = paginator.page(rt.cursor / PER_PAGE + 1)
                except EmptyPage:
                    errors.append({'code':'badResumptionToken', 'msg':'The resumptionToken "%s" is invalid.' % resumption_token})
        except ResumptionToken.DoesNotExist:
            errors.append({'code':'badResumptionToken', 'msg':'The resumptionToken "%s" is invalid.' % resumption_token})
        check_bad_arguments(params, errors, msg='The usage of resumptionToken as an argument allows no other arguments.')
    else:
        paginator = Paginator(objs, PER_PAGE)
        page = paginator.page(1)
    return (paginator, page)
