from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^scorecard/front/(?P<iso3>\w+)/$', direct_to_template, {"template" : "oda/scorecard_front.html"}, "scorecard_front"),
    (r'^scorecard/back/(?P<iso3>\w+)/$', direct_to_template, {"template" : "oda/scorecard_back.html"}, "scorecard_back"),
    (r'^data/country_name/(?P<iso3>\w+)/$', 'oda.views.data_country_name', {}, "data_country_name"),
    (r'^data/allocation/(?P<iso3>\w+)/$', 'oda.views.data_allocation', {}, "data_allocation"),
    (r'^data/(?P<iso3>\w+)/$', 'oda.views.country_data', {}, "country_data"),
)
