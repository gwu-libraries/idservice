from django.contrib import admin

from lidapp.models import Requester, Minter, ID


class RequesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organization', 'date_created']
    list_filter = ['date_created']
    search_fields = ['name', 'organization']
admin.site.register(Requester, RequesterAdmin)


class MinterAdmin(admin.ModelAdmin):
    list_display = ['id', 'authority_number', 'prefix', 'template',
        'minter_type', 'date_created']
    list_filter = ['date_created', 'minter_type', 'authority_number']
admin.site.register(Minter, MinterAdmin)


class IDAdmin(admin.ModelAdmin):
    list_display = ['id', 'identifier', 'id_type', 'minter',
        'requester', 'object_type', 'object_url']
    list_filter = ['date_created', 'date_updated', 'requester', 'minter',
        'object_type']
    search_fields = ['identifier', 'object_url', 'description']
admin.site.register(ID, IDAdmin)

