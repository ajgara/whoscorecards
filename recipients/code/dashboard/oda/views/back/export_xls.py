from tablib import Dataset, Databook
from django.http.response import HttpResponse
from django.views.generic.base import View
import re
import oda.models as models
from oda.views.back.disbursement_sources import BilateralDisbursementSourcesTable, MultilateralAndFoundationDisbursementSourcesTable
from oda.views.back.five_largest import FiveLargestGraph
from oda.views.back.largest_disbursement import LargestDisbursementTable


class ExportBackDataAsXLS(View):
    def bilateral_table_data_sheet(self):
        work_sheet = Dataset(title="Bilateral")
        work_sheet.headers = ['iso', 'country', 'number of disbursements', 'total shown disbursement', 'total real disbursement']

        for country in models.Recipient.objects.all():
            table = BilateralDisbursementSourcesTable(country=country).as_dictionary()

            if len(table):
                number = table["total"]["number_of_disbursements"]
                amount_formatted = table["total"]["amount"]["formatted"]
                amount_real = table["total"]["amount"].get("real", '')
                work_sheet.append([country.iso3, country.name, number, amount_formatted, amount_real])

        return work_sheet

    def multilateral_and_foundation_table_data_sheet(self):
        work_sheet = Dataset(title="Multilateral-Foundation")
        work_sheet.headers = ['iso', 'country', 'number of disbursements', 'total shown disbursement', 'total real disbursement']

        for country in models.Recipient.objects.all():
            table = MultilateralAndFoundationDisbursementSourcesTable(country=country).as_dictionary()

            if len(table):
                number = table["total"]["number_of_disbursements"]
                amount_formatted = table["total"]["amount"]["formatted"]
                amount_real = table["total"]["amount"].get("real", '')
                work_sheet.append([country.iso3, country.name, number, amount_formatted, amount_real])

        return work_sheet

    def five_largest_graph_data_sheet(self):
        work_sheet = Dataset(title="Five Largest Graph")
        work_sheet.headers = ['iso', 'country', 'position', 'shown percentage', 'real percentage', 'donor']

        for country in models.Recipient.objects.all():
            table = FiveLargestGraph(country=country).as_list()
            for position, disbursement in enumerate(table):
                real = disbursement["percentage"]["real"]
                formatted = disbursement["percentage"]["formatted"]
                donor = disbursement["name"]
                work_sheet.append([country.iso3, country.name, position + 1, formatted, real, donor])

        return work_sheet

    def seven_largest_single_data_sheet(self):
        work_sheet = Dataset(title="7 Largest Disbursements")
        work_sheet.headers = ['iso', 'country', 'position', 'shown amount', 'shown donor']

        for country in models.Recipient.objects.all():
            table = LargestDisbursementTable(country=country).as_dictionary()["table"]

            for position, disbursement in enumerate(table):
                formatted = disbursement["disbursement"]
                donor = disbursement["donor"]
                work_sheet.append([country.iso3, country.name, position + 1, formatted,  donor])

        return work_sheet

    def other_disbursements_data_sheet(self):
        work_sheet = Dataset(title="Other disbursements")
        work_sheet.headers = ['iso', 'country', 'amount of other disbursements vs 7 largest']

        for country in models.Recipient.objects.all():
            re_disb = re.compile("Other (\d+) Disb\s*")
            disbursements = models.Disbursement.objects.filter(country=country)
            other_disbursements = disbursements.get(donor__contains="Other ")
            ndisb = int(re_disb.match(other_disbursements.donor).groups()[0])

            total_disbursements_count = disbursements.count() - 1 + ndisb
            work_sheet.append([country.iso3, country.name, total_disbursements_count])

        return work_sheet

    def get(self, request):
        book = Databook()
        book.add_sheet(self.bilateral_table_data_sheet())
        book.add_sheet(self.multilateral_and_foundation_table_data_sheet())
        book.add_sheet(self.five_largest_graph_data_sheet())
        book.add_sheet(self.seven_largest_single_data_sheet())
        book.add_sheet(self.other_disbursements_data_sheet())

        response = HttpResponse(book.xls, mimetype='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % u"back_data"

        return response
