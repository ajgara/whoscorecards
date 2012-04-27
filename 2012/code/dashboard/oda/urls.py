from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^scorecard/front/$', "oda.views.scorecard_front", {}, "scorecard_front"),
)
