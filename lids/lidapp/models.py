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

    def _generate_id(self):
        # Currently only generates ARKs
        if self.minter_type == 'a':
            return arkpy.mint(authority=self.authority_number, prefix=self.prefix, template=self.template)

    def _id_exists(self, identifier):
        res = ID.objects.filter(identifier=identifier)
        return True if len(res) > 0 else False

    def mint(self, requester, quantity=1):
        ids = []
        for i in range(int(quantity)):
            identifier = self._generate_id()
            while self._id_exists(identifier):
                identifier = self._generate_id()
            id = ID.objects.create(identifier=identifier, minter=self, id_type=self.minter_type,
                                   requester=requester, date_created=datetime.now())
            ids.append(id)
        return ids


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

    bindable_fields = ['object_url','object_type','description']

    def __unicode__(self):
        return self.identifier

    def bind(self, **kwargs):     
        for var in kwargs:
            if var in self.bindable_fields:
                setattr(self, var, kwargs[var])
        self.date_updated = datetime.now()
        self.save()

    def to_dict(self):
        return {'identifier':self.identifier,
                'date_created':str(self.date_created),
                'date_updated':str(self.date_updated),
                'id_type':self.id_type,
                'minter':str(self.minter),
                'requester':str(self.requester),
                'object_url':self.object_url,
                'object_type':self.object_type,
                'description':self.description}
