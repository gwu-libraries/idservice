from django.conf.urls.defaults import patterns, include, url
from lidapp.views import mint, bind, lookup, form


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^mint/(?P<minter>\w)/(?P<quantity>[1-9][0-9]{0,2})(\d)?$',mint),
    url(r'^mint/(?P<minter>\w)?$', form, {'action':'mint'}),

    url(r'^bind/(?P<id>\w)$', bind),
    url(r'^bind/', form, {'action':'bind'}),                   

    url(r'^lookup/(?P<id>\w)$',lookup),
    url(r'^lookup/$', form, {'action':'lookup'}),

    url(r'^/$', form),
)
