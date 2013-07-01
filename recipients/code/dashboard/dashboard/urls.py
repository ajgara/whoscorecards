from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.static import serve

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dashboard.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^oda/', include('oda.urls')),
)

#if settings.DEBUG:
#    urlpatterns += patterns('',
#        (r'^site_media/(?P<path>.*)$', serve, {'document_root': '/path/to/media'}),
#    )
