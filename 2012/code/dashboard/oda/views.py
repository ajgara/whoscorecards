import re 
from django.views.generic.simple import direct_to_template
from django.template.loader import render_to_string
from django.template import loader, Context
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
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

def data_allocation(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    allocations = models.Allocation.objects.filter(country=country)
    js = json.dumps( [{
        'mdgpurpose' : a.mdgpurpose.pk,
        'commitment' : a.commitment,
        'disbursement' : a.disbursement,
        'year' : a.year,
    } for a in allocations])
    
    return HttpResponse(js)

def country_data(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    indicators = models.CountryIndicator.objects.filter(country=country)
    js = json.dumps( [{
        'indicator' : i.indicator.pk,
        'value' : i.value,
        'year' : i.year,
    } for i in indicators])
    
    return HttpResponse(js)

def all_data(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    from itertools import groupby
    indicators = groupby(
        models.CountryIndicator.objects.filter(country=country).order_by("year", "indicator__pk"),
        lambda x : x.year
    )

    allocations = groupby(
        models.Allocation.objects.filter(country=country).order_by("year", "mdgpurpose"),
        lambda x : x.year
    )

    js = {
        "country" : {
            "name" : country.name,
            "iso3" : country.iso3,
        }, 
        "indicators" : {
            year : {
                i.indicator.pk : i.value
                for i in it
            }
            for year, it in indicators 
        },
        "allocations" : {
            year : [
            {
                'mdgpurpose' : a.mdgpurpose.pk,
                'commitment' : a.commitment,
                'disbursement' : a.disbursement
            } for a in it ]
            for year, it in allocations
        },
    }
    
    return HttpResponse(json.dumps(js, indent=4))

def back_data(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    re_disb = re.compile("Other (\d+) Disb\s*")
    
    total = models.DisbursementSource.objects.filter(country=country).aggregate(Sum('amount'))["amount__sum"]
    disbursements = models.Disbursement.objects.filter(country=country)
    other_disbursements = disbursements.get(donor__contains="Other ")
    ndisb = int(re_disb.match(other_disbursements.donor).groups()[0])
    pdisb = other_disbursements.percentage
    total_disbursements_count = disbursements.count() - 1 + ndisb
    total_disbursements_sum = disbursements.aggregate(Sum('disbursement'))

    js = {
        "country" : {
            "name" : country.name,
            "iso3" : country.iso3,
        }, 
        "summary" : {
            "total_disbursements_count" : total_disbursements_count,
            "total_disbursements_sum" : total_disbursements_sum,
        },
        "bil_sources" : {
            ds.source : {
                "number": ds.number,
                "amount": ds.amount
            }
            for ds in models.DisbursementSource.objects.filter(country=country, group="Bil")
        },
        "mul_sources" : {
            ds.source : {
                "number": ds.number,
                "amount": ds.amount
            }
            for ds in models.DisbursementSource.objects.filter(country=country, group="Mul")
        },
        "largest_sources" : [{
               "percentage" : ds.amount / total,
               "source" : ds.source 
            }
            for ds in models.DisbursementSource.objects.filter(country=country).order_by("-amount")[0:5]
        ],
        "largest_disbursements" : [{
               "donor" : d.donor, 
               "year" : d.year, 
               "disbursement" : d.disbursement, 
               "purpose" : d.purpose, 
            }
            for d in disbursements.exclude(donor__contains="Other ").order_by("-disbursement")[0:7]
        ],
        "disbursements_percentage" : {
            "other" : {"number" : ndisb, "percentage" : pdisb},
            "largest" : {"number" : 7, "percentage" : 1 - pdisb},
        }
    }
    
    return HttpResponse(json.dumps(js, indent=4))
