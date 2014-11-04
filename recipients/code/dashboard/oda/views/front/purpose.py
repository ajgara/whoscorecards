import oda.models as models


class Purpose(object):
    def __init__(self, allocation):
        self.allocation = allocation

    @property
    def year(self):
        return self.allocation.year

    @property
    def name(self):
        return self.allocation.mdgpurpose.name

    @property
    def values(self):
        raise Exception(u"Subclass responsibility.")

    @classmethod
    def default_value(cls):
        return {'formatted': '-'}


class CommitmentPurpose(Purpose):
    @property
    def values(self):
        formatted = '{:,.2f}'.format(self.allocation.commitment)
        real = self.allocation.commitment
        return {'real': real, 'formatted': formatted}


class DisbursementPurpose(Purpose):
    @property
    def values(self):
        formatted = '{:,.2f}'.format(self.allocation.disbursement)
        real = self.allocation.disbursement
        return {'real': real, 'formatted': formatted}


class PurposeTable(object):
    TOTAL_PURPOSE_NAME = 'Total'

    def __init__(self):
        self.table_data = self.generate_empty_table_data()
        self.fill_table_data()

    @property
    def years(self):
        return sorted(set([indicator.year for indicator in self.allocations]))

    @property
    def purpose_names(self):
        purpose_list = ['HEALTH POLICY & ADMIN. MANAGEMENT',
                        'MDG6',
                        'Other Health Purposes',
                        'RH & FP',
                        'Total']

        if not self.TOTAL_PURPOSE_NAME == purpose_list[-1]:
            raise Exception(u"Total must be last in purpose list.")

        purposes_in_db = models.MDGPurpose.objects.all().values_list('name', flat=True)
        if not all([i in purposes_in_db for i in purpose_list[:-1]]):
            raise Exception(u"All purposes in list must be in the database except for the total.")

        return purpose_list

    def generate_empty_table_data(self):
        data = {}
        for year in self.years:
            if not year in data.keys():
                data[year] = {}
            for purpose_name in self.purpose_names:
                data[year][purpose_name] = Purpose.default_value()
        return data

    def fill_table_data(self):
        raise Exception(u"Subclass responsibility")

    def as_dictionary(self):
        table_data = {
            'years': self.years,
            'data': self.table_data,
            'names': self.purpose_names
        }
        return table_data


class CommitmentPurposeTable(PurposeTable):
    def __init__(self, country):
        self.allocations = models.Allocation.objects.filter(country=country, commitment__isnull=False)
        super(CommitmentPurposeTable, self).__init__()

    def fill_table_data(self):
        for allocation in self.allocations:
            purpose = CommitmentPurpose(allocation)
            self.table_data[purpose.year][purpose.name] = purpose.values

        for year in self.years:
            total = sum([x['real'] for x in self.table_data[year].values() if 'real' in x])
            formatted = '{:,.2f}'.format(total)
            values = {'formatted': formatted, 'real': total}
            self.table_data[year][self.TOTAL_PURPOSE_NAME] = values


class DisbursementPurposeTable(PurposeTable):
    def __init__(self, country):
        self.allocations = models.Allocation.objects.filter(country=country, disbursement__isnull=False)
        super(DisbursementPurposeTable, self).__init__()

    def fill_table_data(self):
        for allocation in self.allocations:
            purpose = DisbursementPurpose(allocation)
            self.table_data[purpose.year][purpose.name] = purpose.values

        for year in self.years:
            total = sum([x['real'] for x in self.table_data[year].values() if 'real' in x])
            formatted = '{:,.2f}'.format(total)
            values = {'formatted': formatted, 'real': total}
            self.table_data[year][self.TOTAL_PURPOSE_NAME] = values