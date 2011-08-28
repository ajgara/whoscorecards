import sys
import os
import dataprocessing
from processutils import process_svg_template, none_is_zero, fmt_pop, fmt_1000, fmt_perc, fmt_r0, fmt_r1, fmt_r2

donor_svg = "../svg/WHO_ODA_donar.svg"
output_path = "gen_donors"

is_donor1 = lambda donor : lambda x : x.donorname_e == donor
is_donor2 = lambda donor : lambda x : x.DONOR == donor

class DonorCountry(object):
    def __init__(self, country, db_donor_data, db_donor_oda):
        self.country = country
        self._donor_data = db_donor_data.data / is_donor1(country)
        self._donor_oda = db_donor_oda.data / is_donor2(country)

        # Years are presented as ranges - e.g. 2000-2002
        # Return only the end of the range
        self.fn_clean_year = lambda x : x.split("-")[1]

    @property
    def oda_commitments(self):
        f_oda = "Total ODA By DONOR - three years MovAv"
        f_year = "Three Years"


        fn_get_commitments = lambda x : (self.fn_clean_year(x[f_year]), x[f_oda])
        oda_commitments =  dict(self._donor_oda * fn_get_commitments)
        return oda_commitments

    @property
    def oda_health(self):
        f_oda = "HEALTH ODA By DONOR three years MovAv"
        f_year = "Three Years"

        fn_get_health_oda = lambda x : (self.fn_clean_year(x[f_year]), x[f_oda])
        oda_health =  dict(self._donor_oda * fn_get_health_oda)
        return oda_health

    @property
    def oda_health_perc(self):
        oda = self.oda_commitments
        oda_health = self.oda_health

        return {
            year : oda_health[year] / oda[year] for year in oda.keys()
        }

class ProcessingException(Exception):
    pass

def process_commitments_table(donor_country, template_xml):

    data = {}
    dc = donor_country

    oda_commitments = dc.oda_commitments
    oda_health = dc.oda_health
    oda_health_perc = dc.oda_health_perc
    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        data["oda_%s" % y] = fmt_r1(oda_commitments[year])
        data["odah_%s" % y] = fmt_r1(oda_health[year])
        data["odahp_%s" % y] = fmt_perc(oda_health_perc[year])

    template_xml = process_svg_template(data, template_xml)
    return template_xml

def process_donor_country(donor_country):
    template_xml = open(donor_svg, "r").read().decode("utf-8")

    dc = donor_country
    data = {
        "country" : dc.country 
    }
    template_xml = process_svg_template(data, template_xml)
    template_xml = process_commitments_table(dc, template_xml)

    f = open("%s/%s.svg" % (output_path, dc.country), "w")
    f.write(template_xml.encode("utf-8"))
    f.close()

def main(*args):

    try:
        recipient_indicators = dataprocessing.load_data("recipient_indicators")
        db_donor_data = dataprocessing.load_data("donor_data")
        db_donor_oda = dataprocessing.load_data("donor_oda")
    except dataprocessing.DataProcessingException, e:
        print >> sys.stderr, e.message
        cleanup()

    #for country in open("../data/recipient/recipients"):
    for country in ["France"]:
        country = country.strip()
        if country.startswith("#"): continue
        #if os.path.exists("gen_donors/%s.svg" % country):
        #    continue
        print "Processing: %s" % country
        try:
            dc = DonorCountry(country, db_donor_data, db_donor_oda)
            process_donor_country(dc)
        except ProcessingException, e:
            print "Skipping %s due to processing exception: %s" % (country, e.message)

if __name__ == "__main__":
    main(*sys.argv)
