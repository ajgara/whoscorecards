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

def front_data(request, iso3):
    country = get_object_or_404(models.Recipient, iso3=iso3) 
    country_indicators = models.CountryIndicator.objects.filter(country=country)
    allocations = models.Allocation.objects.filter(country=country)

    hd_indicator = models.GeneralIndicator.objects.get(name="ODA for Health Disbursements (Million constant 2009 US$)")
    mdg6_purpose = models.MDGPurpose.objects.get(name="MDG6")
    
    # summary calculations
    hd_2000 = country_indicators.get(year="2000", indicator=hd_indicator)
    hd_2010 = country_indicators.get(year="2010", indicator=hd_indicator)
    p_2000 = allocations.get(year="2000", mdgpurpose=mdg6_purpose)
    p_2010 = allocations.get(year="2010", mdgpurpose=mdg6_purpose)

    sum_increase = (hd_2010.value / hd_2000.value - 1) * 100
    mdg6_perc_2000 = (p_2000.disbursement / hd_2000.value) * 100
    mdg6_perc_2010 = (p_2010.disbursement / hd_2010.value) * 100

    indicators = defaultdict(dict, {})
    for indicator in country_indicators:
        indicators[indicator.year][indicator.indicator.name] = indicator.value

    allocations_commitments = defaultdict(dict, {})
    allocations_disbursements = defaultdict(dict, {})
    for allocation in allocations:
        allocations_commitments[allocation.year][allocation.mdgpurpose.name] = allocation.commitment;
        allocations_disbursements[allocation.year][allocation.mdgpurpose.name] = allocation.disbursement;

    js = {
        "country" : {
            "name" : country.name,
            "iso3" : country.iso3,
        }, 
        "summary" : {
            "sum_increase" : sum_increase,
            "sum_amount" : mdg6_perc_2010,
            "sum_2000" : mdg6_perc_2000,
        },
        "indicators" : indicators,
        "allocations" : {
            "commitments" : allocations_commitments,
            "disbursements" : allocations_disbursements,
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
    total_disbursements_sum = float(disbursements.aggregate(Sum('disbursement'))["disbursement__sum"])

    js = {
        "country" : {
            "name" : country.name,
            "iso3" : country.iso3,
        }, 
        "summary" : {
            "total_disbursements_count" : total_disbursements_count,
            "total_disbursements_sum" : total_disbursements_sum,
            "total_disbursements_from_largest" : total,
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
