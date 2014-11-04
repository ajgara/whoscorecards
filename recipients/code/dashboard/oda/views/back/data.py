from itertools import chain
import json
import re
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import oda.models as models


BILATERAL_SOURCE_NAME = 'Bil'
MULTILATERAL_SOURCE_NAME = 'Mul'
FOUNDATION_SOURCE_NAME = 'Phil'


def get_all_disbursement_sources():
    bilateral, multilateral, foundation = set([]), set([]), set([])

    for disbursement_source in models.DisbursementSource.objects.all():
        if disbursement_source.group == BILATERAL_SOURCE_NAME:
            bilateral.add(disbursement_source.source)
        elif disbursement_source.group == MULTILATERAL_SOURCE_NAME:
            multilateral.add(disbursement_source.source)
        elif disbursement_source.group == FOUNDATION_SOURCE_NAME:
            foundation.add(disbursement_source.source)

    return sorted(bilateral), sorted(multilateral), sorted(foundation)

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

    bilateral, multilateral, foundation = get_all_disbursement_sources()

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
        "all_disbursement_sources": {
            "bilateral": bilateral,
            "multilateral": multilateral,
            "foundation": foundation,
        },
        "bil_sources" : {
            ds.source : {
                "number": ds.number,
                "amount": ds.amount
            }
            for ds in models.DisbursementSource.objects.filter(country=country, group=BILATERAL_SOURCE_NAME)
        },
        "mul_sources" : {
            ds.source : {
                "number": ds.number,
                "amount": ds.amount
            }
            for ds in models.DisbursementSource.objects.filter(country=country, group=MULTILATERAL_SOURCE_NAME)
        },
        "phil_sources" : {
            ds.source : {
                "number": ds.number,
                "amount": ds.amount
            }
            for ds in models.DisbursementSource.objects.filter(country=country, group=FOUNDATION_SOURCE_NAME)
        },
        "largest_sources" : [{
               "percentage" : ds.percentage,
               "source" : ds.donor
            }
            for ds in chain(
                models.Largest5Disbursements.objects\
                    .filter(country=country)\
                    .exclude(donor__startswith="Other")\
                    .order_by("-percentage"),
                models.Largest5Disbursements.objects.filter(country=country, donor__startswith="Other")
            )
        ],
        "largest_disbursements" : [{
               "donor" : d.donor,
               "year" : int(float(d.year)),
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