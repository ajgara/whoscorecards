import json
import oda.models as models
from django.conf import settings


class IndicatorCreator(object):
    GENERIC_INDICATOR_NAMES = {
        'Population': 'Population as at 30 June',
        'ODA Commitments Total': 'Commitments TOTAL ODA (Million Constant 2013 US$)',
        'ODA Disbursements Total': 'Disbursements TOTAL ODA (Million Constant 2013 US$)',
        'ODA Commitments Health': 'ODA for Health Commitments, (Million, Constant 2013 US$)',
        'ODA Disbursements Health': 'ODA for Health Disbursements, (Million, Constant 2013 US$)',
        'ODA Commitments Ratio Health/Total': 'RATIO Health/Total ODA Commitments',
        'ODA Disbursements Ratio Health/Total': 'RATIO Health/Total ODA Disbursements',
        'Health Commitments per Capita': 'Health Commitments per Capita',
        'Health Disbursements per Capita': 'Health Disbursements per Capita',
        'Regional Avg Health Commitments per Capita': 'Regional avg Health Commitments per Capita (const.2013 US$)',
        'Regional Avg Health Disbursements per Capita': 'Regional avg Health Disbursements per Capita (const.2013 US$)',
        'Total Expenditure on Health': 'Total expenditure on Health (curr US$ p.c.)',
        'Government Expenditure on Health': 'General government expenditure on Health (curr US$ p.c.)',
        'Private Expenditure on Health': 'Private expenditure on Health (curr US$ p.c.)',
    }

    @classmethod
    def generic_indicator_names(cls):
        indicators_in_db = models.GeneralIndicator.objects.all().values_list('name', flat=True)
        if not all([i in indicators_in_db for i in cls.GENERIC_INDICATOR_NAMES.values()]):
            raise Exception(u"Some indicators are missing in GENERIC_INDICATOR_NAMES dictionary.")
        return {value: key for key, value in cls.GENERIC_INDICATOR_NAMES.items()}

    @classmethod
    def create_from(cls, country_indicator):
        indicator_name = cls.generic_indicator_names()[country_indicator.indicator.name]

        if indicator_name in ['Population']:
            return PopulationIndicator(country_indicator)
        else:
            return GeneralIndicator(country_indicator)


class Indicator(object):
    def __init__(self, country_indicator):
        self.indicator = country_indicator

    def formatted_value(self):
        raise Exception(u"Subclass responsibility.")

    def real_value(self):
        if self.indicator.value:
            return self.indicator.value

    @property
    def name(self):
        return IndicatorCreator.generic_indicator_names()[self.indicator.indicator.name]

    @property
    def year(self):
        return self.indicator.year

    @property
    def values(self):
        values = {'formatted': self.formatted_value()}
        if self.real_value():
            values['real'] = self.real_value()
        return values

    @classmethod
    def default_value(cls):
        return {'formatted': '-'}


class PopulationIndicator(Indicator):
    def formatted_value(self):
        if self.indicator.value:
            return '{:,.2f}'.format(self.indicator.value / 1000000)
        else:
            if self.indicator.raw_value.startswith('<'):
                return self.indicator.raw_value
        return '-'


class GeneralIndicator(Indicator):
    def formatted_value(self):
        if self.indicator.value:
            return '{:,.2f}'.format(self.indicator.value)
        else:
            if self.indicator.raw_value.startswith('<'):
                return self.indicator.raw_value
        return '-'


class IndicatorTable(object):
    def __init__(self, country):
        self.indicators = models.CountryIndicator.objects.filter(country=country)
        self.table_data = self.generate_empty_table_data()
        self.fill_table_data()

    @property
    def years(self):
        return map(str, range(settings.FIRST_YEAR, settings.LAST_YEAR + 1))

    @property
    def indicator_names(self):
        indicators_list = ['Population',
                           'ODA Commitments Total',
                           'ODA Disbursements Total',
                           'ODA Commitments Health',
                           'ODA Disbursements Health',
                           'ODA Commitments Ratio Health/Total',
                           'ODA Disbursements Ratio Health/Total',
                           'Health Commitments per Capita',
                           'Health Disbursements per Capita',
                           'Regional Avg Health Commitments per Capita',
                           'Regional Avg Health Disbursements per Capita',
                           'Total Expenditure on Health',
                           'Government Expenditure on Health',
                           'Private Expenditure on Health']
        indicators = IndicatorCreator.generic_indicator_names().values()
        if not all([i in indicators for i in indicators_list]):
            raise Exception(u"Some indicators are missing in the ordered list of indicators for table 1.")
        return indicators_list

    def generate_empty_table_data(self):
        data = {}
        for year in self.years:
            if not year in data.keys():
                data[year] = {}
            for indicator_name in self.indicator_names:
                data[year][indicator_name] = Indicator.default_value()
        return data

    def fill_table_data(self):
        for country_indicator in self.indicators:
            indicator = IndicatorCreator.create_from(country_indicator)
            self.table_data[indicator.year][indicator.name] = indicator.values

    def as_dictionary(self):
        table_info = {
            'years': self.years,
            'names': self.indicator_names,
            'data': self.table_data
        }
        return table_info