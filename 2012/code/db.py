import xlrd
import ftypes

class DataProcessingException(Exception):
    pass

class SheetReader(object):
    def __init__(self, sheet):
        self._sheet = sheet
        def get_data():
            for i in range(self._sheet.nrows):
                row = self._sheet.row(i)
                r = map(lambda x : x.value, row)
                yield r
        self._data = ftypes.list(*get_data())

    @property
    def data(self):
        return self._data

class XLSDB(object):
    def get_data_sheet(self, file_name, sheet_name):
        try:
            book = xlrd.open_workbook(file_name)
        except IOError:
            print >> sys.stderr, "Could not open %" (file_name)
            raise DataProcessingException("Could not open %s" % file_name)
            
        try:
            return book.sheet_by_name(sheet_name)
        except xlrd.XLRDError:
            print >> sys.stderr, "Could not open sheet: %s in %s" % (sheet_name, file_name)
            raise DataProcessingException("Could not open sheet %s in %s" % (sheet_name, file_name))

    def load_data(self, file_name, sheet_name):
        return SheetReader(
            self.get_data_sheet(file_name, sheet_name)
        )


class FListMixin(object):
    def __init__(self, data):
        self.data = data

    def filter(self, func):
        return FListMixin(self.data / func)

    def __str__(self):
        return "\n".join(map(str, self.data))

    def __getitem__(self, idx):
        return self.data[idx]

class PurposeDBFactory(XLSDB):
    def __init__(self, file_path="../data/Purpose of ODA.xls", sheet_name="DB"):
        super(PurposeDBFactory, self).__init__()
        self.file_path = file_path
        self.data = self.load_data(file_path, sheet_name).data

    def get_purpose_for_country(self, iso3):
        country_data = self.data / (lambda x : x["ISO3"] == iso3)
        return RecipientODAPurpose(iso3, country_data)

class RecipientODAPurpose(FListMixin):
    def __init__(self, iso3, data):
        self.iso = iso3
        self.data = data

    def by_year(self, year):
        return self.data / (lambda x : x["Year"] == year)
