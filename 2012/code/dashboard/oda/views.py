from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import json
from collections import defaultdict

import models

def country_data(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    indicators = models.CountryIndicator.objects.filter(country=country)
    years = defaultdict(dict, {})
    for indicator in indicators:
        year = years[indicator.year]
        year[indicator.indicator.id] = indicator.value
    
    return HttpResponse(json.dumps(years))
     

