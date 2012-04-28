from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from collections import defaultdict

import models

def data_country_name(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    data = [{
        "Name" : country.name, 
        "ISO3" : country.iso3
    }]
    return HttpResponse(json.dumps(data))

def country_data(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    indicators = models.CountryIndicator.objects.filter(country=country)
    js = json.dumps( [{
        'indicator' : i.indicator.pk,
        'value' : i.value,
        'year' : i.year,
    } for i in indicators])
    
    return HttpResponse(js)

