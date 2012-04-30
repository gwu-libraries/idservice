from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
)
    
urlpatterns += patterns('lidapp.views',

    (r'^mint/(?P<minter_name>\w+)/(?P<quantity>[1-9]\d{0,2})$', 'mint'),
    (r'^bind/(?P<identifier>\w+/\w+)$', 'bind'),
    (r'^lookup/(?P<identifier>\w+/\w+)$', 'lookup'),
    (r'^(?P<identifier>\w+/\w+)$', 'resolve'),

)

