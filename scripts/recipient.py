import sys
import xlrd
import ftypes

data_files = {
    "recipient_indicators" : "../data/recipient/recipient_indicators.xls",
    "donor_data"           : "../data/recipient/donor_data2.xls",
}

sheet_names = {
    "recipient_data" : "Sheet2",
    "donor_data"     : "DataBase",
}

is_country = lambda country : lambda x : x.ISO3 == country 

class RecipientCountry(object):
    def __init__(self, iso3, recipient_indicators, donor_data):
        self._recipient_indicators = recipient_indicators.data / is_country(iso3)
        self._donor_data = donor_data.data / is_country(iso3)

        self.colmap = {
            "population"      : "all ages",
            "oda_commitments" : "MovAverage",
            "oda_health"      : "Total",
            "oda_regional"    : "3 yrs Mova average",
            "oda_health_perc" : "ODA/Health as % ODA",
            "oda_health_per_capita" : "ODA/Health as % ODA",
            "total_health"    : "Total expenditure on health / capita at exchange rate",
            "general_health"  : "General government expenditure on health (GGHE) as % of THE",
            "mdg6"            : "MDG6",
            "rhfp"            : "RH & FP",
            "other_health"    : "Other health purposes",
            "unspecified"     : "Unspecified",
        }

    def _yearzip(self, data):
        year = self._recipient_indicators.Year
        return dict(zip(year, data))

    def __getattr__(self, attr_key):
        if attr_key in self.colmap:
            data_key = self.colmap[attr_key]

            coldata = self._recipient_indicators.__getattr__(data_key)
            return self._yearzip(coldata)
        else:
            return object.__getattribute__(self, attr_key)

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

def cleanup():
    sys.exit()

def get_data_sheet(fname, sname):
    try:
        book = xlrd.open_workbook(fname)
    except IOError:
        print >> sys.stderr, "Could not open %" (fname)
        cleanup() 
        
    try:
        return book.sheet_by_name(sname)
    except xlrd.XLRDError:
        print >> sys.stderr, "Could not open sheet: %s in %s" % (sname, fname)
        cleanup() 

def main(*args):
    indicator_file = open(data_files["recipient_indicators"])
    book = data_sheet = None

        
    recipient_indicators = SheetReader(
        get_data_sheet(data_files["recipient_indicators"], sheet_names["recipient_data"])
    )

    sources_data = SheetReader(
        get_data_sheet(data_files["donor_data"], sheet_names["donor_data"])
    )

    ethiopia = RecipientCountry("ETH", recipient_indicators, sources_data)

    for c in ["population", "oda_commitments", "oda_health", "oda_health_perc", "oda_health_per_capita", "oda_regional", "total_health", "general_health"]:
        vals = ethiopia.__getattr__(c)
        print c,
        for year in range(2002, 2010):
            print vals[str(year)],
        print ""

if __name__ == "__main__":
    main(*sys.argv)
