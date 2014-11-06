from itertools import chain
import json
import re
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import oda.models as models
from oda.views.back.disbursement_sources import BilateralDisbursementSourcesTable, MultilateralAndFoundationDisbursementSourcesTable
from oda.views.back.five_largest import FiveLargestGraph
from oda.views.back.largest_disbursement import LargestDisbursementTable


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

    bilateral_table = BilateralDisbursementSourcesTable(country)
    multilateral_and_foundation_table = MultilateralAndFoundationDisbursementSourcesTable(country)
    five_largest_graph = FiveLargestGraph(country)
    largest_disbursement_table = LargestDisbursementTable(country)

    js = {
        "bilateral_table": bilateral_table.as_dictionary(),
        "multilateral_and_foundation_table": multilateral_and_foundation_table.as_dictionary(),
        "five_largest_graph": five_largest_graph.as_list(),
        "largest_disbursement_table": largest_disbursement_table.as_list(),
        "country" : {
            "name" : country.name,
            "iso3" : country.iso3,
        },
        "summary" : {
            "total_disbursements_count" : total_disbursements_count,
            "total_disbursements_sum" : total_disbursements_sum,
            "total_disbursements_from_largest" : total,
        },
        "disbursements_percentage" : {
            "other" : {"number" : ndisb, "percentage" : pdisb},
            "largest" : {"number" : 7, "percentage" : 1 - pdisb},
        }
    }

    return HttpResponse(json.dumps(js, indent=4))