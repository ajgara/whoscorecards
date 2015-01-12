from collections import defaultdict
import json
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from oda.utils import safe_mul, safe_div
import oda.models as models
from oda.views.front.indicators_table import IndicatorTable
from oda.views.front.purpose import CommitmentPurposeTable, DisbursementPurposeTable


class FrontDataView(View):
    def get(self, request, iso3):
        country = get_object_or_404(models.Recipient, iso3=iso3)
        country_indicators = models.CountryIndicator.objects.filter(country=country)
        allocations = models.Allocation.objects.filter(country=country)

        hd_indicator = models.GeneralIndicator.objects.get(
            name="ODA for Health Disbursements, (Million, Constant 2012 US$)"
        )

        overrides = {
            "BLR" : "2005",
            "LBY" : "2005",
            "MNE" : "2004",
	    "SSD" : "2011", #Added by BSG
            "UKR" : "2005",
        }

        base_year = "2002"
        last_year = "2012"

        if country.iso3 in overrides:
            base_year = overrides[country.iso3]
        # summary calculations
        try:
            hd_base_year = country_indicators.get(year=base_year, indicator=hd_indicator)
            hd_base_year = hd_base_year.value
        except models.CountryIndicator.DoesNotExist:
            hd_base_year = 0

        try:
            hd_last_year = country_indicators.get(year=last_year, indicator=hd_indicator)
            hd_last_year = hd_last_year.value
        except models.CountryIndicator.DoesNotExist:
            hd_last_year = 0

        # Highest valued allocation in last year
        alloc_last_year = allocations.filter(year=last_year).order_by("-disbursement")[0]
        mdg_purpose = alloc_last_year.mdgpurpose
        try:
            alloc_base_year = allocations.get(year=base_year, mdgpurpose=mdg_purpose)
        except models.Allocation.DoesNotExist:
            alloc_base_year = models.Allocation()
            alloc_base_year.disbursement = 0

        sum_increase = (hd_last_year / hd_base_year - 1) * 100
        mdg_perc_base_year = safe_mul(safe_div(alloc_base_year.disbursement, hd_base_year), 100)
        mdg_perc_last_year = safe_mul(safe_div(alloc_last_year.disbursement, hd_last_year), 100)

        indicators = defaultdict(dict, {})
        for indicator in country_indicators:
            if indicator.value:
                indicators[indicator.year][indicator.indicator.name] = indicator.value
            else:
                # Value could start with '<', for example '<0.5'. Do not use for calculations
                if indicator.raw_value.startswith("<"):
                    indicators[indicator.year][indicator.indicator.name] = indicator.raw_value

        indicator_table = IndicatorTable(country)
        commitment_purpose_table = CommitmentPurposeTable(country)
        disbursement_purpose_table = DisbursementPurposeTable(country)

        js = {
            "country" : {
                "name" : country.name,
                "iso3" : country.iso3,
            },
            "summary" : {
                "sum_increase" : abs(sum_increase),
                "sum_label" : "increased" if sum_increase > 0 else "decreased",
                "sum_purpose" : mdg_purpose.name,
                "sum_last_year" : mdg_perc_last_year,
                "sum_base_year" : mdg_perc_base_year,
                "sum_baseyear" : base_year,
            },
            "indicator_table": indicator_table.as_dictionary(),
            "commitment_purpose_table": commitment_purpose_table.as_dictionary(),
            "disbursement_purpose_table": disbursement_purpose_table.as_dictionary(),
        }
        return HttpResponse(json.dumps(js, indent=4))
