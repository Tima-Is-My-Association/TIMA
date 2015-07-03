from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from oai_pmh.models import Header, MetadataFormat, ResumptionToken

@csrf_exempt
def oai2(request):
    """
    Handels all OAI-PMH v2 requets. For details see
    https://www.openarchives.org/OAI/openarchivesprotocol.html
    """

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
        else:
            errors.append({'code':'badVerb', 'msg':'The verb "%s" provided in the request is illegal.' % verb})
    else:
        errors.append({'code':'badVerb', 'msg':'The request does not provide any verb.'})
    return render(request, template if not errors else 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')

def checkBadArguments(p, errors):
    for param in p:
        errors.append({'code':'badArgument', 'msg':'The argument "%s" (value="%s") included in the request is not valid.' % (param, p[param])})

