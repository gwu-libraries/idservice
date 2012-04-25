from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from lidapp.models import ID, Minter, Requester
import json

def _ids_to_json(ids):
    return json.dumps([id.dump_dict() for id in ids], indent=2)

def mint(request, minter_name, quantity=1):
    minter = get_object_or_404(Minter, name=minter_name)
    requester = get_object_or_404(Requester, name=request.GET['requester'])
    ids = minter.mint(requester=requester, quantity=quantity)
    return HttpResponse(_ids_to_json(ids), content_type='application/json')
        
def bind(request, identifier):
    id = get_object_or_404(ID, identifier=identifier)
    kwargs = {}
    for field in id.bindable_fields:
        if field in request.GET:
            kwargs[field] = request.GET[field]
    id.bind(**kwargs)
    return HttpResponse(_ids_to_json([id]), content_type='application/json')

def lookup(request, identifier):
    id = get_object_or_404(ID,identifier=identifier)
    return HttpResponse(_ids_to_json([id]), content_type='application/json')

def resolve(request, identifier):
    id = get_object_or_404(ID,identifier=identifier)
    if id.object_url:
        url = id.object_url if id.object_url.startswith('http://') else 'http://'+id.object_url
        return redirect(url)
