import oda.models as models
import re


class LargestDisbursementTable(object):
    def __init__(self, country):
        self.country = country
        self.disbursements = models.Disbursement.objects.filter(country=country).exclude(donor__contains="Other ").order_by("-disbursement")[0:7]

    def table_as_list(self):
        data = []
        for disbursement in self.disbursements:
            formatted_disbursement = '$' + '{:,.2f}'.format(disbursement.disbursement) + 'm'
            data.append({
                'donor': disbursement.donor.upper(),
                'year': int(float(disbursement.year)),  # Year is stored as 2012.0 ???????
                'disbursement': formatted_disbursement,
                'purpose': disbursement.purpose
            })
        return data

    def graph_info(self):
        other_disbursements = models.Disbursement.objects.filter(country=self.country).get(donor__contains="Other ")
        regular_exp_disbursement = re.compile("Other (\d+) Disb\s*")
        number_other_disbursements = int(regular_exp_disbursement.match(other_disbursements.donor).groups()[0])
        percentage_disbursement = other_disbursements.percentage
        data = {
            'other': {
                'number': number_other_disbursements,
                'percentage': {
                    'formatted': '{:,.0f}'.format(percentage_disbursement * 100),
                    'real': percentage_disbursement
                }
            },
            'largest': {
                'number': 7,
                'percentage': {
                    'formatted': '{:,.0f}'.format((1 - percentage_disbursement) * 100),
                    'real': percentage_disbursement
                }
            }
        }
        return data

    def as_dictionary(self):
        data = {
            'table': self.table_as_list(),
            'graph': self.graph_info()
        }
        return data