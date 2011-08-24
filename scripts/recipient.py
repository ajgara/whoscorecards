import sys
import xlrd
import ftypes

data_files = {
    "recipient_indicators" : "../data/recipient/recipient_indicators.xls",
    "donor_data"           : "../data/recipient/donor_data3.xls",
}

sheet_names = {
    "recipient_data" : "Sheet2",
    "donor_data"     : "DataBase",
}

recipient_svg = "../svg/WHO_ODA_recipient.svg"
donor_svg = "../svg/WHO_ODA_donar.svg"

recipient_indicators = None
sources_data = None

is_country = lambda country : lambda x : x.ISO3 == country 

class RecipientCountry(object):
    def __init__(self, iso3, recipient_indicators, donor_data):
        self._recipient_indicators = recipient_indicators.data / is_country(iso3)
        self._donor_data = donor_data.data / is_country(iso3)
        self.country = self._recipient_indicators[0]["WHO Name"]

        self.colmap = {
            "population"      : "all ages",
            "oda_commitments" : "MovAverage",
            "oda_health"      : "Total",
            "oda_regional"    : "3 yrs Mova average",
            "oda_health_perc" : "ODA/Health as % ODA",
            "oda_health_per_capita" : "USD Per capita",
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

    @property
    def bilateral_donations(self):
        is_mdg = lambda x : x.__getattr__("MDG Purpose")
        
        mdg_donations = self._donor_data / is_mdg
        donors = mdg_donations.__getattr__("donorname_e")
        print donors
        print mdg_donations.__getattr__("2007-2009")
        return mdg_donations

    def __getattr__(self, attr_key):
        if attr_key in self.colmap:
            data_key = self.colmap[attr_key]

            coldata = self._recipient_indicators.__getattr__(data_key)
            return self._yearzip(coldata)
        elif attr_key in ["mdg6_perc", "rhfp_perc", "other_health_perc", "unspecified_perc"]:
            new_key = attr_key.replace("_perc", "")
            num_arr = self.__getattr__(new_key)
            den_arr = self.__getattr__("oda_health")
            return { year : (num_arr[year] / den_arr[year]) for year in num_arr.keys()}
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

def process_svg_template(context, template):
    country = context["country"]
    filename = "generated/%s.svg" % country
    new_svg_file = open(filename, 'wb')

    # no need to make it difficult with xml parsing
    # just do find/replace
    svg_data = open(template).read()
    for (key, value) in context.items():
        svg_data = svg_data.replace('{%s}' % key, value)
    new_svg_file.write(svg_data)
    new_svg_file.close()

    return filename

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

def process_recipient_country(country):
    rc = recipient_country = RecipientCountry(country, recipient_indicators, sources_data)
    fmt_pop = lambda x : str(round(x / 1000000.0, 1))
    fmt_r1 = lambda x : "{:,.1f}".format(x)
    #fmt_r1 = lambda x : str(round(x, 1))
    fmt_perc = lambda x : str(round(x * 100, 1))
    fmt_r2 = lambda x : str(round(x, 2))
    fmt_r0 = lambda x : str(round(x, 0))

    data = {
        "country" : recipient_country.country 
    }
    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        data["pop_%s" % y] = fmt_pop(rc.population[year])
        data["oda_%s" % y] = fmt_r1(rc.oda_commitments[year])
        data["odah_%s" % y] = fmt_r1(rc.oda_health[year])
        data["odahp_%s" % y] = fmt_perc(rc.oda_health_perc[year])
        data["odahc_%s" % y] = fmt_r1(rc.oda_health_per_capita[year])
        data["odahr_%s" % y] = fmt_r2(rc.oda_regional[year])
        data["the_%s" % y] = fmt_r2(rc.total_health[year])
        data["gh_%s" % y] = fmt_r1(rc.general_health[year])
        data["mdg6_%s" % y] = "%s (%s%%)" % (fmt_r1(rc.mdg6[year]), fmt_perc(rc.mdg6_perc[year]))
        data["rhfp_%s" % y] = "%s (%s%%)" % (fmt_r1(rc.rhfp[year]), fmt_perc(rc.rhfp_perc[year]))
        data["ohp_%s" % y] = "%s (%s%%)" % (fmt_r1(rc.other_health[year]), fmt_perc(rc.other_health_perc[year]))
        data["unspec_%s" % y] = "%s (%s%%)" % (fmt_r1(rc.unspecified[year]), fmt_perc(rc.unspecified_perc[year]))
    print data
    process_svg_template(data, recipient_svg)

    recipient_country.bilateral_donations

def main(*args):
    global recipient_indicators, sources_data

    indicator_file = open(data_files["recipient_indicators"])
    book = data_sheet = None

        
    recipient_indicators = SheetReader(
        get_data_sheet(data_files["recipient_indicators"], sheet_names["recipient_data"])
    )

    sources_data = SheetReader(
        get_data_sheet(data_files["donor_data"], sheet_names["donor_data"])
    )

    for country in ["ETH"]:
        process_recipient_country(country)
    


if __name__ == "__main__":
    main(*sys.argv)
