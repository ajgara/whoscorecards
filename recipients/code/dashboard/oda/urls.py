from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from oda.views.front.data import FrontDataView


def urlroute(to_url, view, name):
    return url(to_url, view, name=name)

urlpatterns = patterns('',
    urlroute(
        to_url=r'^scorecard/front/(?P<iso3>\w+)/$', 
        view=TemplateView.as_view(template_name='oda/scorecard_front.html'), 
        name="scorecard_front"
    ),
    urlroute(
        to_url=r'^scorecard/back/(?P<iso3>\w+)/$',
        view=TemplateView.as_view(template_name='oda/scorecard_back.html'),
        name="scorecard_back"
    ),
    urlroute(
        to_url=r'^scorecard/(?P<iso3>\w+)/',
        view='oda.views.scorecard.scorecard',
        name=""
    ),
    #(r'^data/country_name/(?P<iso3>\w+)/$', 'oda.views.data_country_name', {}, "data_country_name"),
    #(r'^data/allocation/(?P<iso3>\w+)/$', 'oda.views.data_allocation', {}, "data_allocation"),
    #(r'^data/(?P<iso3>\w+)/$', 'oda.views.country_data', {}, "country_data"),
    urlroute(
        to_url=r'^data/(?P<iso3>\w+)/front_data/$',
        view=FrontDataView.as_view(),
        name="front_data"
    ),
    urlroute(
        to_url=r'^data/(?P<iso3>\w+)/back_data/$',
        view='oda.views.back.data.back_data',
        name="back_data"
    ),
)
