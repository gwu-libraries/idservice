from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from idapp.models import ID
from services import arks

ID_ATTRIBUTES = ['id_type','path','description','owner']

def mint(request, quantity=1):
    #TODO: Add expriation date to minted ids? 
    if not quantity.isdigit():
        return HttpResponseBadRequest('The quantity requested was not a valid integer.')
    ids = arks.mint(quantity=quantity, owner=HttpRequest.get_host())
    output = ''
    for id in ids:
        output += id + '\n'
    return HttpResponse(output.rstrip())
        

def bind(request, id):
    #TODO: Add interface/form for manual update
    #TODO: Add error handling
    kwargs = {}
    for attribute in ID_ATTRIBUTES:
        if attribute in request.POST:
            kwargs[attribute] = request.POST[attribute]
    results = arks.bind(id, **kwargs)
    return HttpResponse(_format_id_list(results))


def lookup(request, id):
    return HttpResponse(_format_id_list(arks.lookup(id)))


def _format_id_list(ids):
    output = ''
    for id in ids:
        line = 'identifier:%s, ' % (id.identifier)
        for attribute in ID_ATTRIBUTES:
            line += '%s:%s, ' % (attribute, getattr(id, attribute))
        output += line.rstrip([, ])+'\n'
    return output.rstrip()
