import oda.models as models
from itertools import chain


class DisbursementSource(object):
    def __init__(self, disbursement_source):
        self.disbursement_source = disbursement_source

    @property
    def values(self):
        formatted = '{:,.2f}'.format(self.disbursement_source.amount)
        data = {
            'number_of_disbursements': self.disbursement_source.number,
            'amount': {
                'formatted': formatted,
                'real': self.disbursement_source.amount,
            }
        }
        return data

    @classmethod
    def default_value(cls):
        data = {
            'number_of_disbursements': '-',
            'amount': {
                'formatted': '-'
            }
        }
        return data


class DisbursementSourcesTable(object):
    TOTAL_SOURCE_NAME = 'TOTAL'

    def __init__(self, country):
        self.country = country
        self.table_data = self.generate_empty_table_data()
        self.fill_table_data()

    def generate_empty_table_data(self):
        data = {}
        sources_names = self.get_all_disbursement_sources_names()
        sources_names.append(self.TOTAL_SOURCE_NAME)

        for disbursement_source_name in sources_names:
            data[disbursement_source_name] = DisbursementSource.default_value()

        return data

    def fill_table_data(self):
        number = 0
        amount = 0
        disbursement_sources = self.get_country_disbursement_sources()
        for disbursement_source in disbursement_sources:
            values = DisbursementSource(disbursement_source).values
            number += disbursement_source.number
            amount += float(values['amount']['formatted'])
            self.table_data[disbursement_source.source] = values

        if len(disbursement_sources) > 0:
            data = {
                'number_of_disbursements': number,
                'amount': {
                    'formatted': '{:,.2f}'.format(amount),
                    'real': amount,
                }
            }

            self.table_data[self.TOTAL_SOURCE_NAME] = data

    def get_all_disbursement_sources_names(self):
        raise Exception(u"Subclass responsibility.")

    def get_country_disbursement_sources(self):
        raise Exception(u"Subclass responsibility.")

    def as_dictionary(self):
        sources_names = self.get_all_disbursement_sources_names()
        sources_names.append(self.TOTAL_SOURCE_NAME)

        data = {
            'sources': sources_names,
            'data': self.table_data
        }
        return data


class BilateralDisbursementSourcesTable(DisbursementSourcesTable):
    BILATERAL_SOURCE_NAME = 'Bil'

    def get_all_disbursement_sources_names(self):
        bilateral = set([])
        for disbursement_source in models.DisbursementSource.objects.all():
            if disbursement_source.group == self.BILATERAL_SOURCE_NAME:
                bilateral.add(disbursement_source.source)
        return sorted(bilateral)

    def get_country_disbursement_sources(self):
        return models.DisbursementSource.objects.filter(country=self.country, group=self.BILATERAL_SOURCE_NAME)


class MultilateralAndFoundationDisbursementSourcesTable(DisbursementSourcesTable):
    MULTILATERAL_SOURCE_NAME = 'Mul'
    FOUNDATION_SOURCE_NAME = 'Phil'

    def get_all_disbursement_sources_names(self):
        multilateral = set([])
        foundation = set([])
        for disbursement_source in models.DisbursementSource.objects.all():
            if disbursement_source.group == self.MULTILATERAL_SOURCE_NAME:
                multilateral.add(disbursement_source.source)
            elif disbursement_source.group == self.FOUNDATION_SOURCE_NAME:
                foundation.add(disbursement_source.source)
        return sorted(multilateral) + sorted(foundation)

    def get_country_disbursement_sources(self):
        multilateral = models.DisbursementSource.objects.filter(country=self.country, group=self.MULTILATERAL_SOURCE_NAME)
        foundation = models.DisbursementSource.objects.filter(country=self.country, group=self.FOUNDATION_SOURCE_NAME)
        return list(chain(multilateral, foundation))