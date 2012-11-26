from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'who.views.home', name='home'),
    # url(r'^who/', include('who.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^data/(?P<donor>[^/]*)/disbursements/$', 'oda.views.json_disbursements'),
    url(r'^data/(?P<donor>[^/]*)/purpose/$', 'oda.views.json_purpose'),
    url(r'^data/(?P<donor>[^/]*)/disbursement_by_income/$', 'oda.views.json_disbursement_by_income'),
    url(r'^data/(?P<donor>[^/]*)/disbursement_by_region/$', 'oda.views.json_disbursement_by_region'),
)
