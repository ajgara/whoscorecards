from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    (r'^scorecard/front/$', direct_to_template, {"template" : "oda/scorecard_front.html"}, "scorecard_front"),
    (r'^scorecard/back/$', direct_to_template, {"template" : "oda/scorecard_back.html"}, "scorecard_back"),
    (r'^data/(?P<iso3>\w+)/$', 'oda.views.country_data', {}, "country_data"),
)
