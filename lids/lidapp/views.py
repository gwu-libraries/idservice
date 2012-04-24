from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from lidapp.models import ID, Minter, Requester


def mint(request, minter_name, quantity=1):
    minter = get_object_or_404(Minter, name=minter_name)
    requester = get_object_or_404(Requester, name=request.GET['requester'])
    ids = minter.mint(requester=requester, quantity=quantity)
    output = '\n'.join([id.identifier for id in ids])
    return HttpResponse(output)
        
def bind(request, identifier):
    id = get_object_or_404(ID, identifier=identifier)
    atts = {'object_type':None, 'object_url':None, 'description':None}
    for att in atts:
        if att in request.GET:
            atts[att] = request.GET[att]
    id.bind(**atts)
    return render_to_response('id_dump.txt', {'id':id})

def lookup(request, identifier):
    id = get_object_or_404(ID,identifier=identifier)
    return render_to_response('id_dump.txt', {'id':id})

