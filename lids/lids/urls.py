from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('lidapp.views',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

    (r'^mint/(?P<minter_name>\w+)/(?P<quantity>[1-9]\d{0,2})$', 'mint'),
    (r'^bind/(?P<identifier>\w+/\w+)$', 'bind'),
    (r'^lookup/(?P<identifier>\w+/\w+)$', 'lookup'),
    (r'^(?P<identifier>\w+/\w+)$', 'resolve'),

)

