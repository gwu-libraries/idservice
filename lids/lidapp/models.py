from datetime import datetime
from django.db import models
from lids import settings
import arkpy


class Requester(models.Model):

    name = models.CharField(max_length=63)
    organization = models.CharField(max_length=63)
    date_created = models.DateTimeField()
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Minter(models.Model):

    name = models.CharField(max_length=7)
    authority_number = models.CharField(max_length=15)
    prefix = models.CharField(max_length=7, blank=True)
    template = models.CharField(max_length=25, blank=True)
    minter_type = models.CharField(max_length=1, choices=settings.ID_TYPES)
    date_created = models.DateTimeField()
    description = models.TextField()

    def __unicode__(self):
        return self.name


class ID(models.Model):
    
    # System generated fields
    identifier = models.CharField(max_length=25)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)
    id_type = models.CharField(max_length=1, choices=settings.ID_TYPES) #This field is redundant on purpose
    # Required user-specified fields
    minter = models.ForeignKey(Minter, related_name='id_minter')
    requester = models.ForeignKey(Requester, related_name='id_requester')
    # Non-required user-specified fields
    object_url = models.URLField(blank=True)
    object_type = models.CharField(max_length=1, choices=settings.OBJECT_TYPES, blank=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return identifier

    @staticmethod
    def exists(identifier):
        res = ID.objects.filter(identifier=identifier)
        return True if len(res) > 0 else False

    @staticmethod
    def lookup(identifier):
        try:
            id = ID.objects.get(identifier=identifier)
            return id
        except Exception, e:
            return None

    @staticmethod
    def mint(requester_name, minter_name, quantity=1):
        ids = []
        try:
            requester = Requester.objects.get(name=requester_name)
            minter = Minter.objects.get(name=minter_name)
        except Exception, e:
            return ids
        else:
            for i in range(int(quantity)):
                identifier = ID._generate_id(id_type=minter.minter_type, prefix=minter.prefix,
                                             authority_number=minter.authority_number, template=minter.template)
                while ID.exists(identifier):
                    identifier = ID._generate_id(id_type=minter.minter_type, prefix=minter.prefix, 
                                                 authority_number=minter.authority_number, template=minter.template)
                ID.objects.create(identifier=identifier, minter=minter, id_type=minter.minter_type,
                                  requester=requester, date_created=datetime.now())
                ids.append(identifier)
            return ids

    @staticmethod
    def _generate_id(id_type, prefix, authority_number, template):
        if id_type == 'a':
            return arkpy.mint(authority=authority_number, prefix=prefix, template=template)
        ''' Stubs for potential future id types
        elif id_type == 'Handle':
            return handle.mint()
        else:
            return ''
        '''

    @staticmethod
    def bind(identifier, **kwargs):
        try:
            id = ID.objects.get(identifier=identifier)
        except Exception, e:
            return None
        else:
            for att in kwargs.keys():
                if att in ['object_url','object_type','description']:
                    setattr(id, att, kwargs[att])
            id.date_updated = datetime.now()
            id.save()
            return id
