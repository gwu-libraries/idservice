from django.db import models
from lidapp import settings
import datetime
import arkpy


class Log(models.Model):

    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=settings.ACTIONS)
    requester = models.ForeignKey('Requester')
    minter = models.ForeignKey('Minter')
    identifier = models.ForeignKey('ID')
    description = models.textField()


class Requester(models.Model):

    name = models.CharField()
    organization = models.CharField()
    date_created = models.DateTimeField()
    description = models.TextField()


class Minter(models,Model):

    name = models.CharField()
    authority_number = CharField()
    prefix = models.CharField(max_length=7, blank=True)
    template = models.CharField(blank=True)
    minter_type = models.CharField(max_length=1, choices=settings.ID_TYPES)
    date_created = models.DateTimeField()
    description = models.TextField()


class ID(models.Model):
    
    # System generated fields
    identifier = models.CharField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True)
    id_type = models.CharField(max_length=1, choices=settings.ID_TYPES) #This field is redundant on purpose
    # Required user-specified fields
    minter = models.ForeignKey('Minter')
    requester = models.ForeignKey('Requester')
    # Non-required user-specified fields
    object_url = models.URLField(blank=True)
    object_type = models.CharField(max_length=1, choices=settings.OBJECT_TYPES, blank=True)
    description = models.TextField(blank=True)

    def exists(self, identifier):
        res = ID.objects.filter(identifier=identifier)
        if res.count() == 0:
            return False
        return True

    def lookup(self, identifier, requester):
        res = ID.objects.filter(identifier=identifier)
        if res.count() == 0:
            return None
        return res[0]

    def mint(self, requester, minter_name=settings.DEFAULT_MINTER, quantity=1):
        ids = []
        minter = Minter.objects.filter(minter_name=minter_name)
        for range(0, quantity):
            id = generate_id(id_type=minter.id_type, prefix=minter.minter_prefix, authority_number=minter.authority_number, template=minter.template)
            while exists(id):
                id = generate_id(id_type)
            ID.objects.create(identifier=id, requester=requester, date_created=datetime.datetime.now())
            ids.append(id)
        return ids

    def generate_id(self, id_type, prefix, authority_number, template):
        if id_type == 'ark':
            ark = arkpy.mint(authority=authority_number, template=template)
            return ark
        # Stubs for potential future id types
        '''
        elif id_type == 'Handle':
            handle = ''
            return handle
        else:
            return ''
        '''

    def bind(self, identifier, **kwargs):
        id = ID.objects.filter(identifier=identifier)
        for pair in kwargs.items():
            if pair[1] != '' and pair[0] in dir(ID):
                setattr(id, pair[0], pair[1])
        id.save()
        return id
    
