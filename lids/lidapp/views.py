from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import redirect
from django.utils.timezone import now
from lidapp.models import ID, Minter, Requester
import logging
import json

logger = logging.getLogger('lidapp.actions')

def _ids_to_json(ids):
    return json.dumps([id.dump_dict() for id in ids], indent=2)

def mint(request, minter_name, quantity=1):
    ip = request.META['REMOTE_ADDR']
    quantity = int(quantity)
    try:
        requester = Requester.objects.get(ip=ip)
        minter = Minter.objects.get(name=minter_name)
        ids = minter.mint(requester=requester, quantity=quantity)
        for x in range(quantity):
            logger.info('Action: mint %s of %s  IP: %s  Result:SUCCESS.  Minted %s' % (x+1, quantity, ip, ids[x].identifier))
        return HttpResponse(_ids_to_json(ids), content_type='application/json')
    except Requester.DoesNotExist:
        logger.info('Action: mint %s  IP: %s  Result:FAILED. IP not recognized' %(quantity, ip))
        raise Http404('You are not permitted to mint IDs from IP address %s' % ip)
    except Minter.DoesNotExist:
        logger.info('Action: mint %s  IP: %s  Result:FAILED.  Minter %s does not exist' % (quantity, ip, minter_name))
        raise Http404('Minter %s does not exist' % minter_name)
    except Minter.InactiveMinter:
        logger.info('Action: mint %s  IP: %s  Result:FAILED.  Minter %s is inactive' % (quantity, ip, minter_name))
        raise Http404('Minter %s is inactive and cannot mint new identifiers' % minter_name)
        
def bind(request, identifier):
    ip = request.META['REMOTE_ADDR']
    try:
        requester = Requester.objects.get(ip=ip)
        id = ID.objects.get(identifier=identifier)
        if requester.admin == False and not id.requester.ip == requester.ip:
            logger.info('Action: bind  IP: %s  ID: %s  Result:FAILED. Requester not authorized to edit ID' % (ip, identifier))
            return HttpResponseForbidden('You are not authorized to bind data to ID %s from IP address %s' % (identifier, ip))
        kwargs = {}
        for field in id.bindable_fields:
            if field in request.GET:
                kwargs[field] = request.GET[field]
        id.bind(**kwargs)
        logger.info('Action: bind  IP: %s  ID: %s  Result:SUCCESS. Data: %s' % (ip, identifier, kwargs))
        return HttpResponse(_ids_to_json([id]), content_type='application/json')
    except Requester.DoesNotExist:
        logger.info('Action: bind  IP: %s  ID: %s  Result:FAILED. IP not recognized' % (ip, identifier))
        raise Http404('You are not permitted to bind IDs from IP address %s' % ip)
    except ID.DoesNotExist:
        logger.info('Action: bind  IP: %s  ID: %s  Result:FAILED. Identifier does not exist' % (ip, identifier))
        raise Http404('ID %s does not exist %s' % identifier)    
    except ID.NoChanges:
        logger.info('Action: bind  IP: %s  ID: %s  Result:FAILED. No changes to bind' % (ip, identifier))
        raise Http404('No changes to the data were included in your request %s' % identifier)
    except ID.NoData:
        logger.info('Action: bind  IP: %s  ID: %s  Result:FAILED. No data to bind' % (ip, identifier))
        raise Http404('No data were included in your request %s' % identifier)

def lookup(request, identifier):
    ip = request.META['REMOTE_ADDR']
    try:
        id = ID.objects.get(identifier=identifier)
        logger.info('Action: lookup  IP: %s  ID: %s  Result:SUCCESS.' % (ip, identifier))
        return HttpResponse(_ids_to_json([id]), content_type='application/json')
    except ID.DoesNotExist:
        logger.info('Action: lookup  IP: %s  ID: %s  Result:FAILED. Identifier does not exist' % (ip, identifier))
        raise Http404('ID %s does not exist %s' % identifier)
    
def resolve(request, identifier):
    try:
        ip = request.META['REMOTE_ADDR']
        id = ID.objects.get(identifier=identifier)
        if id.object_url:
            url = id.object_url if id.object_url.startswith('http') else 'http://'+id.object_url
            logger.info('Action: resolve  IP: %s  ID: %s  Result:SUCCESS.' % (ip, identifier))
            return redirect(url)
        else:
            logger.info('Action: resolve  IP: %s  ID: %s  Result:FAILED. Identifier has not been bound to a url' % (ip, identifier))
            raise Http404('ID %s has not been bound to a url' % identifier)
            #TODO: provide a more graceful resolution error page
    except ID.DoesNotExist:
        logger.info('Action: resolve  IP: %s  ID: %s  Result:FAILED. Identifier does not exist' % (ip, identifier))
        raise Http404('ID %s does not exist' % identifier)
    
