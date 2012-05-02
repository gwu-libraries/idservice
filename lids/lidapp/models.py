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

    def dump_string(self):
        string =  '         name: %s\n' % self.name
        string += ' organization: %s\n' % self.organization
        string += '   IP address: %s\n' % self.ip
        string += 'administrator: %s\n' % self.admin
        string += ' date created: %s\n' % self.date_created 
        string += '  description: %s\n' % self.description
        return string


class Minter(models.Model):

    name = models.CharField(max_length=7, unique=True)
    authority_number = models.CharField(max_length=15, blank=True)
    prefix = models.CharField(max_length=7, blank=True)
    template = models.CharField(max_length=25, blank=True)
    minter_type = models.CharField(max_length=1, choices=settings.ID_TYPES)
    date_created = models.DateTimeField()
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

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

    def dump_string(self):
        string =  '            name: %s\n' % self.name
        string += '     minter type: %s\n' % self.get_minter_type_display()
        string += '    date created: %s\n' % self.date_created
        string += 'authority number: %s\n' % self.authority_number
        string += '          prefix: %s\n' % self.prefix
        string += '        template: %s\n' % self.template
        string += '          active: %s\n' % self.active
        string += '     description: %s\n' % self.description
        return string

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
        if len(kwargs) == 0:
            raise self.NoData()
        changes = 0
        for var in kwargs:
            if var in self.bindable_fields and kwargs[var] != getattr(self, var):
                changes += 1
                setattr(self, var, kwargs[var])
        if changes == 0:
            raise self.NoChanges()
        self.date_updated = now()
        self.save()

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
        string =  '  identifier: %s\n' % self.identifier
        string += '     id type: %s\n' % self.get_id_type_display()
        string += '      minter: %s\n' % self.minter
        string += '   requester: %s\n' % self.requester
        string += 'date created: %s\n' % self.date_created
        string += 'date updated: %s\n' % self.date_updated
        string += ' object type: %s\n' % self.get_object_type_display()
        string += '  object url: %s\n' % self.object_url
        string += ' description: %s\n' % self.description
        return string

    class NoChanges(Exception): pass

    class NoData(Exception): pass
        
