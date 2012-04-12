from datetime import datetime
from django.db import models
from lids import settings
import arkpy


class Requester(models.Model):

    name = models.CharField(max_length=63)
    organization = models.CharField(max_length=63)
    date_created = models.DateTimeField()
    description = models.TextField(blank=True)


class Minter(models.Model):

    name = models.CharField(max_length=7)
    authority_number = models.CharField(max_length=15)
    prefix = models.CharField(max_length=7, blank=True)
    template = models.CharField(max_length=25, blank=True)
    minter_type = models.CharField(max_length=1, choices=settings.ID_TYPES)
    date_created = models.DateTimeField()
    description = models.TextField()


class ID(models.Model):
    
    # System generated fields
    identifier = models.CharField(max_length=25)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True)
    id_type = models.CharField(max_length=1, choices=settings.ID_TYPES) #This field is redundant on purpose
    # Required user-specified fields
    minter = models.ForeignKey(Minter, related_name='id_minter')
    requester = models.ForeignKey(Requester, related_name='id_requester')
    # Non-required user-specified fields
    object_url = models.URLField(blank=True)
    object_type = models.CharField(max_length=1, choices=settings.OBJECT_TYPES, blank=True)
    description = models.TextField(blank=True)

    @staticmethod
    def exists(identifier):
        try:
            res = ID.objects.get(identifier=identifier)
            return True
        except:
            return False

    @staticmethod
    def lookup(identifier, requester_name, requester_ip=''):
        try:
            id = ID.objects.get(identifier=identifier)
            successful, message = True, ''
        except Exception, e:
            id, successful, message = None, False, str(e)            
        finally:
            Log.add_entry(successful=successful, action='l', identifier=identifier,
                          requester_name=requester_name, requester_ip=requester_ip, message=message)
            return id

    @staticmethod
    def mint(requester_name, requester_ip='', minter_name=settings.DEFAULT_MINTER, quantity=1):
        ids = []
        try:
            requester = Requester.objects.get(name=requester_name)
            minter = Minter.objects.get(minter_name=minter_name)
            successful, message = True, ''
        except Exception, e:
            successful, message = False, str(e)
        else:
            for i in range(1, quantity+1):
                qt = str(i) + ' of ' + str(quantity)
                try:
                    suc, msg = True, ''
                    identifier = _generate_id(id_type=minter.id_type, prefix=minter.minter_prefix,
                                                   authority_number=minter.authority_number, template=minter.template)
                    while exists(identifier):
                        identifier = _generate_id(id_type)
                    ID.objects.create(identifier=identifier, minter=minter, requester=requester.id, date_created=datetime.now())
                    ids.append(identifier)
                except Exception, e:
                    suc, msg = False, str(e)
                finally:
                    Log.add_entry(successful=suc,  action='m', identifier=identifier,
                                  requester_name=requester_name, requester_ip=requester_ip,
                                  minter_name=minter.name, quantity=qt, message=msg)
        finally:
            Log.add_entry(successful=successful,  action='m', identifier='',
                          requester_name=requester_name, requester_ip=requester_ip,
                          minter_name=minter_name, quantity=quantity, message=message)
            return ids

    @staticmethod
    def _generate_id(id_type, prefix, authority_number, template):
        if id_type == 'ark':
            ark = arkpy.mint(authority=authority_number, prefix=prefix, template=template)
            return ark
        # Stubs for potential future id types
        '''
        elif id_type == 'Handle':
            handle = ''
            return handle
        else:
            return ''
        '''

    @staticmethod
    def bind(identifier, requester_name, requester_ip='', **kwargs):
        try:
            id = ID.objects.get(identifier=identifier)
            for pair in kwargs.items():
                if pair[1] != '' and pair[0] in ID.__dict__:
                    setattr(id, pair[0], pair[1])
            id.date_updated = datetime.now()
            id.save()
            successful, message = True, ''
        except Exception, e:
            successful, message = False, str(e)
        finally:
            Log.add_entry(successful=successful, action='b', identifier=identifier,
                          requester_name=requester_name, requester_ip=requester_ip,
                          quantity=1, message=message)
            return id

    
class Log(models.Model):

    timestamp = models.DateTimeField()
    identifier = models.CharField(max_length=25, blank=True)
    minter_name = models.CharField(max_length=7, blank=True)
    action = models.CharField(max_length=1, choices=settings.ACTIONS)
    quantity = models.CharField(max_length=12, blank=True)
    requester_name = models.CharField(max_length=63, blank=True)
    requester_ip = models.CharField(max_length=15, blank=True)
    successful = models.BooleanField()
    message = models.TextField(blank=True)

    @staticmethod
    def add_entry(successful, action, identifier='',
                  requester_name='', requester_ip='',
                  minter_name='',quantity='1', message=''):
        timestamp = datetime.now()
        quantity = str(quantity)
        Log.objects.create(**locals())
