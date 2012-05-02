from django.utils.timezone import now
from django.db import models
from lids import settings
import arkpy


class Requester(models.Model):

    name = models.CharField(max_length=63, unique=True)
    organization = models.CharField(max_length=63, blank=True)
    ip = models.IPAddressField(unique=True)
    date_created = models.DateTimeField()
    admin = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Minter(models.Model):

    name = models.CharField(max_length=7, unique=True)
    authority_number = models.CharField(max_length=15)
    prefix = models.CharField(max_length=7, blank=True)
    template = models.CharField(max_length=25, blank=True)
    minter_type = models.CharField(max_length=1, choices=settings.ID_TYPES)
    date_created = models.DateTimeField()
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def get_minter_type(self):
        for pair in settings.ID_TYPES:
            if pair[0] == self.minter_type:
                return pair[1]

    def _generate_id(self):
        # Currently only generates ARKs
        if self.minter_type == 'a':
            return arkpy.mint(authority=self.authority_number, prefix=self.prefix, template=self.template)

    def _id_exists(self, identifier):
        res = ID.objects.filter(identifier=identifier)
        return True if len(res) > 0 else False

    def mint(self, requester, quantity=1):
        if self.active == False:
            raise self.InactiveMinter(self.name)
        ids = []
        for i in range(int(quantity)):
            identifier = self._generate_id()
            while self._id_exists(identifier):
                identifier = self._generate_id()
            id = ID.objects.create(identifier=identifier, minter=self, id_type=self.minter_type,
                                   requester=requester, date_created=now())
            ids.append(id)
        return ids

    class InactiveMinter(Exception):

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return 'Minter "%s" is no longer allowed to mint new idetifiers.' % self.name


class ID(models.Model):
    
    # System generated fields
    identifier = models.CharField(max_length=25, unique=True)
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

    bindable_fields = ['object_url','object_type','description']
    
    def __unicode__(self):
        return self.identifier


    def bind(self, **kwargs):     
        for var in kwargs:
            if var in self.bindable_fields:
                setattr(self, var, kwargs[var])
        self.date_updated = now()
        self.save()

    def get_object_type(self):
        for pair in settings.OBJECT_TYPES:
            if pair[0] == self.object_type:
                return pair[1]

    def get_id_type(self):
        for pair in settings.ID_TYPES:
            if pair[0] == self.id_type:
                return pair[1]

    def dump_dict(self):
        return {'identifier':self.identifier,
                'date_created':str(self.date_created),
                'date_updated':str(self.date_updated),
                'id_type':self.id_type,
                'minter':str(self.minter),
                'requester':str(self.requester),
                'object_url':self.object_url,
                'object_type':self.object_type,
                'description':self.description}

    def dump_string(self):
        string = '  identifier: %s\n' % self.identifier
        string += '     id type: %s\n' % self.get_id_type()
        string += '      minter: %s\n' % self.minter
        string += '   requester: %s\n' % self.requester
        string += 'date created: %s\n' % self.date_created
        string += 'date updated: %s\n' % self.date_updated
        string += ' object type: %s\n' % self.get_object_type()
        string += '  object url: %s\n' % self.object_url
        string += ' description: %s\n' % self.description
        return string
