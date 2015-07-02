from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def oai2(request):
    """
    Handels all OAI-PMH v2 requets. For details see
    https://www.openarchives.org/OAI/openarchivesprotocol.html
    """

    params = request.POST if request.method == 'POST' else request.GET
    p = params.copy()

    if 'verb' in params:
        verb = p.pop('verb')[0]
        if verb == 'Identify':
            if len(p.dict()) == 0:
                return render(request, 'tima/oai_pmh/identify.xml', locals(), content_type='text/xml')
            else:
                errors = []
                for param in p:
                    errors.append({'code':'badArgument', 'msg':'The argument "%s" (value="%s") included in the request is not valid.' % (param, p[param])})
                return render(request, 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')
        else:
            errors = [{'code':'badVerb', 'msg':'The verb "%s" provided in the request is illegal.' % verb}]
            return render(request, 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')
    else:
        errors = [{'code':'badVerb', 'msg':'The request does not provide any verb.'}]
        return render(request, 'tima/oai_pmh/error.xml', locals(), content_type='text/xml')
