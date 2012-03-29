from django.conf.urls.defaults import patterns, include, url
from idapp.views import mint, bind, lookup

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^mint/(\d)?$',mint),
    url(r'^bind/(\w)$',bind),
    url(r'^lookup/(\w)$',lookup),
    
)
