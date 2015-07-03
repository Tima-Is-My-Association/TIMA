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
    params = request.POST if request.method == 'POST' else request.GET
    p = params.copy()

    if 'verb' in params:
        verb = p.pop('verb')[0]
        if verb == 'Identify':
            checkBadArguments(p, errors)
            template = 'tima/oai_pmh/identify.xml'
                return render(request, 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')
        elif verb == 'ListMetadataFormats':
            metadataformats = MetadataFormat.objects.all()

            if 'identifier' in params:
                identifier = p.pop('identifier')[0]
                if Header.objects.filter(identifier=identifier).exists():
                    metadataformats = metadataformats.filter(identifiers__identifier=identifier)
                else:
                    errors.append({'code':'idDoesNotExist', 'msg':'A record with the identifier "%s" does not exist.' % identifier})

            if metadataformats.count() == 0:
                errors.append({'code':'noMetadataFormats', 'msg':'There are no metadata formats available for the record with identifier "%s".' % identifier})
            checkBadArguments(p, errors)
            template = 'tima/oai_pmh/listmetadataformats.xml'
        elif verb == 'ListSets':
            set_list = Set.objects.all()
            template = 'tima/oai_pmh/listsets.xml'

            if set_list.count() == 0:
                errors.append({'code':'noSetHierarchy', 'msg':'This repository does not support sets.'})
            else:
                paginator = Paginator(set_list, PER_PAGE)
                sets = doResumptionToken(params, p, errors, paginator)
            checkBadArguments(p, errors)
        else:
            errors.append({'code':'badVerb', 'msg':'The verb "%s" provided in the request is illegal.' % verb})
    else:
        errors.append({'code':'badVerb', 'msg':'The request does not provide any verb.'})
    return render(request, template if not errors else 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')

def checkBadArguments(p, errors, msg=None):
    for k,v in p.copy().items():
        errors.append({'code':'badArgument', 'msg':'The argument "%s" (value="%s") included in the request is not valid.%s' % (k, v, (' %s' % msg if msg else ''))})
        p.pop(k)

def doResumptionToken(params, p, errors, paginator):
    if 'resumptionToken' in params:
        resumptionToken = p.pop('resumptionToken')[0]
        try:
            rt = ResumptionToken.objects.get(token=resumptionToken)
            if timezone.now() > rt.expiration_date:
                errors.append({'code':'badResumptionToken', 'msg':'The resumptionToken "%s" is expired.' % resumptionToken})
            else:
                try:
                    page = paginator.page(rt.cursor / PER_PAGE + 1)
                except EmptyPage:
                    errors.append({'code':'badResumptionToken', 'msg':'The resumptionToken "%s" is invalid.' % resumptionToken})
        except ResumptionToken.DoesNotExist:
            errors.append({'code':'badResumptionToken', 'msg':'The resumptionToken "%s" is invalid.' % resumptionToken})
        checkBadArguments(p, errors, msg='The usage of resumptionToken as an argument allows no other arguments.')
    else:
        page = paginator.page(1)
    return page
