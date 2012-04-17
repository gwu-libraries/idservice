from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from lidapp.models import ID


def mint(request, minter_name, quantity=1):
    ids = ID.mint(requester_name=request.GET['requester'], minter_name=minter_name, quantity=quantity)
    output = '\n'.join(ids)
    return HttpResponse(output)
        
def bind(request, identifier):
    fields = ['object_type', 'object_url', 'description']
    kwargs = {}
    for attribute in fields:
        if attribute in request.POST:
            kwargs[attribute] = request.POST[attribute]
    id = ID.bind(identifier, **kwargs)
    return render_to_response('id_dump.txt', {'id':id})

def lookup(request, identifier):
    id = get_object_or_404(ID,identifier=identifier)
    return render_to_response('id_dump.txt', {'id':id})

