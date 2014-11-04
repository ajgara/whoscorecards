from tablib import Dataset
from django.http.response import HttpResponse
from django.views.generic.base import View
import oda.models as models
from oda.views.front.indicators_table import IndicatorTable, IndicatorCreator
from oda.views.front.purpose import CommitmentPurposeTable, DisbursementPurposeTable


class ExportTableOneAsXLS(View):
    def get(self, request):
        work_sheet = Dataset()
        work_sheet.headers = ['iso', 'country', 'indicator', 'year', 'real value', 'shown value']

        for country in models.Recipient.objects.all():
            data = IndicatorTable(country).as_dictionary()
            for year in data['years']:
                for indicator in data['names']:
                    indicator_name = IndicatorCreator.GENERIC_INDICATOR_NAMES[indicator]
                    try:
                        real = data['data'][year][indicator]['real']
                    except:
                        real = ''
                    shown = data['data'][year][indicator]['formatted']
                    work_sheet.append([country.iso3, country.name, indicator_name, year, real, shown])

        response = HttpResponse(work_sheet.xls, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % u"table_1"

        return response


class ExportPurposeCommitmentAsXLS(View):
    def get(self, request):
        work_sheet = Dataset()
        work_sheet.headers = ['iso', 'recipient', 'year', 'mdgpurpose', 'real value', 'shown value']

        for country in models.Recipient.objects.all():
            data = CommitmentPurposeTable(country).as_dictionary()
            for year in data['years']:
                for purpose in data['names']:
                    try:
                        real = data['data'][year][purpose]['real']
                    except:
                        real = ''
                    shown = data['data'][year][purpose]['formatted']
                    work_sheet.append([country.iso3, country.name, year, purpose, real, shown])

        response = HttpResponse(work_sheet.xls, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % u"purpose_commitments"

        return response


class ExportPurposeDisbursementAsXLS(View):
    def get(self, request):
        work_sheet = Dataset()
        work_sheet.headers = ['iso', 'recipient', 'year', 'mdgpurpose', 'real value', 'shown value']

        for country in models.Recipient.objects.all():
            data = DisbursementPurposeTable(country).as_dictionary()
            for year in data['years']:
                for purpose in data['names']:
                    try:
                        real = data['data'][year][purpose]['real']
                    except:
                        real = ''
                    shown = data['data'][year][purpose]['formatted']
                    work_sheet.append([country.iso3, country.name, year, purpose, real, shown])

        response = HttpResponse(work_sheet.xls, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % u"purpose_disbursements"

        return response