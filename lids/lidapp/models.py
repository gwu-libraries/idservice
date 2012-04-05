from django.db import models
from lidapp import settings
import datetime
import arkpy

OBJECT_TYPES = (
    ('i', 'item'),
    ('c', 'collection'),
    )

ID_TYPES = (
    ('a', 'ark'),
    #Examples of other IDs we may create in the future
    #('h', 'handle'),
    #('d', 'doi'),
    )

ACTIONS = (
    ('m','mint'),
    ('b','bind'),
    ('l','lookup'),
    )

class Log(models.Model):

    timestamp = models.DateTimeField()
    action = models.CharField(max_length=1, choices=ACTIONS)
    requester = models.ForeignKey('Requester')
    minter = models.ForeignKey('Minter')
    identifier = models.ForeignKey('ID')
    description = models.textField()


class Requester(models.Model):

    name = models.CharField()
    organization = models.CharField()  #TODO: Should I make this a choice list?
    date_created = models.DateTimeField()
    description = models.TextField()


class Minter(models,Model):

    minter_prefix = models.CharField(max_length=7)
    minter_type = models.CharField(max_length=1, choices=ID_TYPES)
    date_created = models.DateTimeField()
    requester = models.ForeignKey('Requester')
    description = models.TextField()


class ID(models.Model):
    
    # System generated fields
    identifier = models.CharField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True)
    id_type = models.CharField(max_length=1, choices=ID_TYPES) #This field is redundant on purpose
    # Required user-specified fields (id type defaults to ARK)
    minter = models.ForeignKey('Minter')
    requester = models.ForeignKey('Requester')
    # Non-required user-specified fields
    object_url = models.URLField(blank=True)
    object_type = models.CharField(max_length=1, choices=OBJECT_TYPES, blank=True)
    description = models.TextField(blank=True)

    def exists(self, identifier):
        res = ID.objects.filter(identifier=identifier)
        if res.count() == 0:
            return False
        return True

    def lookup(self, identifier):
        res = ID.objects.filter(identifier=identifier)
        return res

    def mint(self, requester, minter_prefix=DEFAULT_MINTER, quantity=1):
        ids = []
        minter = Minter.objects.filter(minter_prefix=minter_prefix)
        id_type = minter.minter_type
        for range(1, quantity):
            id = generate_id(id_type=id_type, prefix=minter_prefix)
            while exists(id):
                id = generate_id(id_type)
            ID.objects.create(identifier=id, requester=requester, date_created=datetime.datetime.now())
            arks.append(ark)
        return arks
    
    def generate_id(self, id_type, prefix):
        if id_type == 'ARK':
            ark = arkpy.mint(authority=NMA, template=ARK_TEMPLATE)
            return ark
        # Stubs for potential future id types
        '''
        elif id_type == 'Handle':
            handle = ''
            return handle
        else:
            return ''
        '''

    #TODO: change to bind()
    def update(identifier, **kwargs):
        id = ID.objects.filter(identifier=identifier)
        for pair in kwargs.items():
            if pair[1] != '':
                setattr(id, pair[0], pair[1])
        id.save()
        return id
    
