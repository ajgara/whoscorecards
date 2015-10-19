import oda.models as models
from itertools import chain


class DisbursementSource(object):
    def __init__(self, disbursement_source):
        self.disbursement_source = disbursement_source

    @property
    def values(self):
        formatted = '{:,.2f}'.format(self.disbursement_source.amount)
        data = {
            'name': self.disbursement_source.source,
            'group': self.disbursement_source.group,
            'number_of_disbursements': self.disbursement_source.number,
            'amount': {
                'formatted': formatted,
                'real': self.disbursement_source.amount,
            }
        }
        return data


class DisbursementSourcesTable(object):
    TOTAL_SOURCE_NAME = 'TOTAL'

    def __init__(self, country):
        self.country = country
        self.table_data = {}
        self.fill_table_data()

    def fill_table_data(self):
        number = 0
        amount = 0
        sources = []
        disbursement_sources = self.get_country_disbursement_sources()
        for disbursement_source in disbursement_sources:
            values = DisbursementSource(disbursement_source).values
            number += disbursement_source.number
            amount += disbursement_source.amount
            sources.append(values)

        if len(disbursement_sources) > 0:
            data = {
                'number_of_disbursements': number,
                'amount': {
                    'formatted': '{:,.2f}'.format(amount),
                    'real': amount,
                }
            }

            self.table_data["sources"] = sorted(sources, key=lambda x: x['name'])
            self.table_data["total"] = data

    def get_country_disbursement_sources(self):
        raise Exception(u"Subclass responsibility.")

    def as_dictionary(self):
        return self.table_data


class BilateralDisbursementSourcesTable(DisbursementSourcesTable):
    BILATERAL_SOURCE_NAME = 'Bil'

    def get_country_disbursement_sources(self):
        return models.DisbursementSource.objects.filter(country=self.country, group=self.BILATERAL_SOURCE_NAME)


class MultilateralAndFoundationDisbursementSourcesTable(DisbursementSourcesTable):
    MULTILATERAL_SOURCE_NAME = 'Mul'
    FOUNDATION_SOURCE_NAME = 'Phil'

    def get_country_disbursement_sources(self):
        multilateral = models.DisbursementSource.objects.filter(country=self.country, group=self.MULTILATERAL_SOURCE_NAME)
        foundation = models.DisbursementSource.objects.filter(country=self.country, group=self.FOUNDATION_SOURCE_NAME)
        return list(chain(multilateral, foundation))