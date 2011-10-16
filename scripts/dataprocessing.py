import xlrd
import ftypes
import sys

data_files = {
    #"recipient_indicators": "../data/recipient/recipient_indicators.xls",
    "recipient_indicators" : "../data/recipient/TABLES 1, 2 Correct data.xls",
    #"donor_data"          : "../data/recipient/donor_data3.xls",
    "donor_data"           : "../data/recipient/TABLES 3, 4, 5 NEW DATA.xls",
    #"pivot_for_donors"     : "../data/recipient/TABLES 3, 4, 5 NEW DATA.xls",
    "donor_oda"            : "../data/donor/donor_oda.xls",
    "donation_breakdown"   : "../data/donor/donation_breakdown.xls",
}

sheet_names = {
    #"recipient_indicators" : "Sheet2",
    "recipient_indicators" : "DB",
    "donor_data"           : "DataBase",
    "donor_oda"            : "DB",
    "donation_breakdown"   : "DATA",
}

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


def get_data_sheet(file_name, sheet_name):
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

def load_data(dbname):
    return SheetReader(
        get_data_sheet(data_files[dbname], sheet_names[dbname])
    )

