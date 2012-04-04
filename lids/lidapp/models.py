from django.db import models
import datetime


class ID(models.Model):

    ID_TYPES = (
        ('I', 'Item'),
        ('C', 'Collection'),
        )
    
    identifier = models.CharField(max_length=7)
    id_type = models.CharField(max_length=1, choices=ID_TYPES)
    owner = models.URLField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    path = models.URLField()
    description = models.TextField()

    def exists(identifier):
        res = ID.objects.filter(identifier=identifier)
        if res.count() == 0:
            return False
        return True

    def lookup(identifier):
        res = ID.objects.filter(identifier=identifier)
        return res

    def new(identifier, owner):
        return ID.objects.create(identifier=identifier, owner=owner, date_created=datetime.datetime.now())

    def update(identifier, **kwargs):
        id = ID.objects.filter(identifier=identifier)
        for pair in kwargs.items():
            if pair[1] != '':
                setattr(id, pair[0], pair[1])
        id.save()
        return id
    
