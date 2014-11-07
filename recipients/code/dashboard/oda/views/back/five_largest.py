import oda.models as models


class LargestDisbursement(object):
    def __init__(self, largest_disbursement):
        self.largest_disbursement = largest_disbursement

    @property
    def values(self):
        percentage = self.largest_disbursement.percentage
        formatted = '{:,.1f}'.format(percentage * 100)
        data = {
            'percentage': {
                'formatted': str(formatted) + '%',
                'real': percentage
            },
            'name': self.largest_disbursement.donor
        }
        return data

    @classmethod
    def default_values(cls):
        formatted = '{:,.1f}'.format(0)
        data = {
            'percentage': {
                'formatted': str(formatted) + '%',
                'real': 0
            },
            'name': '-'
        }
        return data


class FiveLargestGraph(object):
    def __init__(self, country):
        self.country = country
        self.largest = models.Largest5Disbursements.objects.filter(country=country).exclude(donor__startswith="Other").order_by("-percentage")

        try:
            self.other = models.Largest5Disbursements.objects.get(country=country, donor__startswith="Other")
        except models.Largest5Disbursements.DoesNotExist:
            self.other = None

    def as_list(self):
        data = []
        for country in self.largest:
            data.append(LargestDisbursement(country).values)

        if self.other:
            data.append(LargestDisbursement(self.other).values)
        else:
            data.append(LargestDisbursement.default_values())

        return data