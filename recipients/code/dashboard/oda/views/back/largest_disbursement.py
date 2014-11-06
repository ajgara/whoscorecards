import oda.models as models


class LargestDisbursementTable(object):
    def __init__(self, country):
        self.disbursements = models.Disbursement.objects.filter(country=country).exclude(donor__contains="Other ").order_by("-disbursement")[0:7]

    def as_list(self):
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