from django.http import HttpResponse
from django.shortcuts import render_to_response
from idapp.models import ID


def mint(request, quantity=1):
    #TODO: Add expriation date to minted ids? 
    ids = ID.mint(quantity=quantity, owner=request.PUT[requester])
    output = '\n'.join(ids)
    return HttpResponse(output)
        
def bind(request, id):
    kwargs = {'object_type':'', 'object_url':'', 'description':'', 'requester':''}
    for attribute in kwargs:
        if attribute in request.POST:
            kwargs[attribute] = request.POST[attribute]
    results = ID.bind(id, **kwargs)
    return render_to_response('id_dump.txt', {'data':results})

def lookup(request, id):
    results = ID.lookup(id, request.POST[requester])
    return render_to_response('id_dump.txt', {'data':results})

def form(request, action, minter=''):
    #TODO: create a form UI for manual input
    pass
