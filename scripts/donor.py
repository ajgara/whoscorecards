from xml.dom import minidom
import numbers
import sys
import os
import dataprocessing
from processutils import process_svg_template, none_is_zero, fmt_pop, fmt_1000, fmt_perc, fmt_perc0, fmt_r0, fmt_r1, fmt_r2, xmlutils
import graphs

donor_svg = "../svg/WHO_ODA_donar.svg"
output_path = "gen_donors"

is_donor1 = lambda donor : lambda x : x.donorname_e == donor
is_donor2 = lambda donor : lambda x : x.DONOR == donor
is_donor3 = lambda donor : lambda x : x.Donor == donor

class DonorCountry(object):
    def __init__(self, country, db_donor_data, db_donor_oda, db_donation_breakdown):
        self.country = country
        self._donor_data = db_donor_data.data / is_donor1(country)
        self._donor_oda = db_donor_oda.data / is_donor2(country)
        self._donation_breakdown = db_donation_breakdown.data / is_donor3(country)

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

    @property
    def ldc_allocation(self):
        f_year = "Period"
        f_allocation = "LDCs,Total (Least Developed)"
        fn_get_ldc_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        ldc_allocation =  dict(self._donation_breakdown * fn_get_ldc_allocation)
        return ldc_allocation

    @property
    def lic_allocation(self):
        f_year = "Period"
        f_allocation = "OLICs,Total (Other Low Income)"
        fn_get_lic_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        lic_allocation =  dict(self._donation_breakdown * fn_get_lic_allocation)
        return lic_allocation

    @property
    def lmi_allocation(self):
        f_year = "Period"
        f_allocation = "LMICs,Total (Low Middle Income)"
        fn_get_lmi_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        lmi_allocation =  dict(self._donation_breakdown * fn_get_lmi_allocation)
        return lmi_allocation

    @property
    def umi_allocation(self):
        f_year = "Period"
        f_allocation = "UMICs,Total (Upper Middle Income)"
        fn_get_umi_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        umi_allocation =  dict(self._donation_breakdown * fn_get_umi_allocation)
        return umi_allocation

    @property
    def gmc_allocation(self):
        f_year = "Period"
        f_allocation = "DONORS TO Income groups 3 yrs MovAv.(blank)"
        fn_get_gmc_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        gmc_allocation =  dict(self._donation_breakdown * fn_get_gmc_allocation)
        return gmc_allocation

    @property
    def afro_allocation(self):
        f_year = "Period"
        f_allocation = "Afr"
        fn_get_afro_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        afro_allocation =  dict(self._donation_breakdown * fn_get_afro_allocation)
        return afro_allocation

    @property
    def amro_allocation(self):
        f_year = "Period"
        f_allocation = "Amr"
        fn_get_amro_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        amro_allocation =  dict(self._donation_breakdown * fn_get_amro_allocation)
        return amro_allocation

    @property
    def emro_allocation(self):
        f_year = "Period"
        f_allocation = "Emr"
        fn_get_emro_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        emro_allocation =  dict(self._donation_breakdown * fn_get_emro_allocation)
        return emro_allocation

    @property
    def euro_allocation(self):
        f_year = "Period"
        f_allocation = "Eur"
        fn_get_euro_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        euro_allocation =  dict(self._donation_breakdown * fn_get_euro_allocation)
        return euro_allocation

    @property
    def searo_allocation(self):
        f_year = "Period"
        f_allocation = "Sear"
        fn_get_searo_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        searo_allocation =  dict(self._donation_breakdown * fn_get_searo_allocation)
        return searo_allocation

    @property
    def wpro_allocation(self):
        f_year = "Period"
        f_allocation = "Wpr"
        fn_get_wpro_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        wpro_allocation =  dict(self._donation_breakdown * fn_get_wpro_allocation)
        return wpro_allocation

    @property
    def gmcr_allocation(self):
        f_year = "Period"
        f_allocation = "Multicount"
        fn_get_gmcr_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        gmcr_allocation =  dict(self._donation_breakdown * fn_get_gmcr_allocation)
        return gmcr_allocation

    @property
    def other_allocation(self):
        f_year = "Period"
        f_allocation = "Not UN"
        fn_get_other_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        other_allocation =  dict(self._donation_breakdown * fn_get_other_allocation)
        return other_allocation

    @property
    def mdg6_allocation(self):
        f_year = "Period"
        f_allocation = "MDG6"
        fn_get_mdg6_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        mdg6_allocation =  dict(self._donation_breakdown * fn_get_mdg6_allocation)
        return mdg6_allocation

    @property
    def rhfp_allocation(self):
        f_year = "Period"
        f_allocation = "RH & FP"
        fn_get_rhfp_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        rhfp_allocation =  dict(self._donation_breakdown * fn_get_rhfp_allocation)
        return rhfp_allocation

    @property
    def otherh_allocation(self):
        f_year = "Period"
        f_allocation = "Other Health Purposes"
        fn_get_otherh_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        otherh_allocation =  dict(self._donation_breakdown * fn_get_otherh_allocation)
        return otherh_allocation

    @property
    def unspecified_allocation(self):
        f_year = "Period"
        f_allocation = "DONORS Purpose 3 yrs MovAv.(blank)"
        fn_get_unspecified_allocation = lambda x : (self.fn_clean_year(x[f_year]), x[f_allocation])
        unspecified_allocation =  dict(self._donation_breakdown * fn_get_unspecified_allocation)
        return unspecified_allocation

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

def process_income_group_table(donor_country, template_xml):
    data = {}
    dc = donor_country

    ldc_allocation = dc.ldc_allocation
    lic_allocation = dc.lic_allocation
    lmi_allocation = dc.lmi_allocation
    umi_allocation = dc.umi_allocation
    gmc_allocation = dc.gmc_allocation
    other_allocation = dc.other_allocation

    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        data["ldc_%s" % y] = fmt_r1(ldc_allocation[year])
        data["lic_%s" % y] = fmt_r1(lic_allocation[year])
        data["lmi_%s" % y] = fmt_r1(lmi_allocation[year])
        data["umi_%s" % y] = fmt_r1(umi_allocation[year])
        data["gmc_%s" % y] = fmt_r1(gmc_allocation[year])
        data["othr_%s" % y] = fmt_r1(other_allocation[year])

    template_xml = process_svg_template(data, template_xml)
    return template_xml

def process_region_table(donor_country, template_xml):
    data = {}
    dc = donor_country

    afro_allocation = dc.afro_allocation
    amro_allocation = dc.amro_allocation
    emro_allocation = dc.emro_allocation
    euro_allocation = dc.euro_allocation
    searo_allocation = dc.searo_allocation
    wpro_allocation = dc.wpro_allocation
    gmcr_allocation = dc.gmcr_allocation

    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        data["afro_%s" % y] = fmt_r1(afro_allocation[year])
        data["amro_%s" % y] = fmt_r1(amro_allocation[year])
        data["emro_%s" % y] = fmt_r1(emro_allocation[year])
        data["euro_%s" % y] = fmt_r1(euro_allocation[year])
        data["searo_%s" % y] = fmt_r1(searo_allocation[year])
        data["wpro_%s" % y] = fmt_r1(wpro_allocation[year])
        data["gmcr_%s" % y] = fmt_r1(gmcr_allocation[year])

    template_xml = process_svg_template(data, template_xml)
    return template_xml

def process_health_table(donor_country, template_xml):
    data = {}
    dc = donor_country

    mdg6_allocation = dc.mdg6_allocation
    rhfp_allocation = dc.rhfp_allocation
    otherh_allocation = dc.otherh_allocation
    unspecified_allocation = dc.unspecified_allocation
    oda_health = dc.oda_health

    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        total = oda_health[year]
        data["mdg_%s" % y] = "%s (%s%%)" % (fmt_r1(mdg6_allocation[year]), fmt_perc0(mdg6_allocation[year] / total))
        data["rf_%s" % y] = "%s (%s%%)" % (fmt_r1(rhfp_allocation[year]), fmt_perc0(rhfp_allocation[year] / total))
        data["oth_%s" % y] = "%s (%s%%)" % (fmt_r1(otherh_allocation[year]), fmt_perc0(otherh_allocation[year] / total))
        data["uns_%s" % y] = "%s (%s%%)" % (fmt_r1(unspecified_allocation[year]), fmt_perc0(unspecified_allocation[year] / total))

    template_xml = process_svg_template(data, template_xml)

    xml = minidom.parseString(template_xml.encode("utf-8"))
    circle_y = 534
    for year, circle_x in [(2002, 164), (2003, 208), (2004, 250), (2005, 293.4), (2006, 336.4), (2007, 379.38), (2008, 422.9), (2009, 466)]:
        year = str(year)
        chart = graphs.PieChart(xml, (circle_x, circle_y), 17, [
            mdg6_allocation[year], 
            rhfp_allocation[year], 
            otherh_allocation[year], 
            unspecified_allocation[year]]
        )
        chart.generate_xml()
    return xml.toxml()

def process_commitments_graph(donor_country, template_xml):
    data = {}
    dc = donor_country
    graph = graphs.BarGraph(num_ticks=7, min_height=285.5, max_height=223)

    oda_commitments = dc.oda_commitments
    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        graph.add_value(year, oda_commitments[year])

    has_data = isinstance(max(graph.values.values()), numbers.Number)
    if not has_data:
        # No data available for this graph
        return template_xml

    g1_ticks = graph.ticks
    data["g1_t1"] = fmt_r0(g1_ticks[1])
    data["g1_t2"] = fmt_r0(g1_ticks[2])
    data["g1_t3"] = fmt_r0(g1_ticks[3])
    data["g1_t4"] = fmt_r0(g1_ticks[4])
    data["g1_t5"] = fmt_r0(g1_ticks[5])
    data["g1_t6"] = fmt_r0(g1_ticks[6])
    data["g1_t7"] = fmt_r0(g1_ticks[7])

    template_xml = process_svg_template(data, template_xml)

    xml = minidom.parseString(template_xml.encode("utf-8"))
    graph.update_bars(xml, {
        2002 : "g1_b2",
        2003 : "g1_b3",
        2004 : "g1_b4",
        2005 : "g1_b5",
        2006 : "g1_b6",
        2007 : "g1_b7",
        2008 : "g1_b8",
        2009 : "g1_b9",
    })

    return xml.toxml()

def process_income_group_graph(donor_country, template_xml):
    data = {}
    dc = donor_country

    ldc_allocation = dc.ldc_allocation
    lic_allocation = dc.lic_allocation
    lmi_allocation = dc.lmi_allocation
    umi_allocation = dc.umi_allocation
    gmc_allocation = dc.gmc_allocation

    xml = minidom.parseString(template_xml.encode("utf-8"))
    for year, circle_x in [(2002, 640.29999), (2003, 693.5), (2004, 746.70001), (2005, 800), (2006, 640.29999), (2007, 693.5), (2008, 746.70001), (2009, 800)]:
        y = str(year)[3]
        if year <= 2005: circle_y = 173.39999
        else: circle_y = 228.3
        year = str(year)
        chart = graphs.PieChart(xml, (circle_x, circle_y), 22.1, [
            ldc_allocation[year], 
            lic_allocation[year], 
            lmi_allocation[year], 
            umi_allocation[year],
            gmc_allocation[year],
        ], colours=["#df7627", "#cf3d96", "#62a73b", "#79317f", "#0093d5"])
        chart.generate_xml()
        black_circle = xmlutils.get_el_by_id(xml, "g", "bcg_%s" % y)
        xml.documentElement.removeChild(black_circle)
        xml.documentElement.appendChild(black_circle)
    return xml.toxml()

def process_region_graph(donor_country, template_xml):
    data = {}
    dc = donor_country

    graph = graphs.BarGraph(num_ticks=9, min_height=285.5, max_height=223)

    afro_allocation = dc.afro_allocation
    amro_allocation = dc.amro_allocation
    emro_allocation = dc.emro_allocation
    euro_allocation = dc.euro_allocation
    searo_allocation = dc.searo_allocation
    wpro_allocation = dc.wpro_allocation
    gmcr_allocation = dc.gmcr_allocation
    oda_health = dc.oda_health

    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        graph.add_value(year, oda_health[year])

    has_data = isinstance(max(graph.values.values()), numbers.Number)
    if not has_data:
        # No data available for this graph
        return template_xml

    g1_ticks = graph.ticks
    data["g2_t1"] = fmt_r0(g1_ticks[1])
    data["g2_t2"] = fmt_r0(g1_ticks[2])
    data["g2_t3"] = fmt_r0(g1_ticks[3])
    data["g2_t4"] = fmt_r0(g1_ticks[4])
    data["g2_t5"] = fmt_r0(g1_ticks[5])
    data["g2_t6"] = fmt_r0(g1_ticks[6])
    data["g2_t7"] = fmt_r0(g1_ticks[7])
    data["g2_t8"] = fmt_r0(g1_ticks[8])
    data["g2_t9"] = fmt_r0(g1_ticks[9])

    template_xml = process_svg_template(data, template_xml)

    xml = minidom.parseString(template_xml.encode("utf-8"))
    graph.update_bars(xml, {
        2002 : "g2_b2",
        2003 : "g2_b3",
        2004 : "g2_b4",
        2005 : "g2_b5",
        2006 : "g2_b6",
        2007 : "g2_b7",
        2008 : "g2_b8",
        2009 : "g2_b9",
    })

    return xml.toxml()

def process_donor_country(donor_country):
    template_xml = open(donor_svg, "r").read().decode("utf-8")

    dc = donor_country
    data = {
        "country" : dc.country 
    }
    template_xml = process_svg_template(data, template_xml)
    template_xml = process_commitments_table(dc, template_xml)
    template_xml = process_income_group_table(dc, template_xml)
    template_xml = process_region_table(dc, template_xml)
    template_xml = process_health_table(dc, template_xml)
    template_xml = process_commitments_graph(dc, template_xml)
    template_xml = process_income_group_graph(dc, template_xml)
    template_xml = process_region_graph(dc, template_xml)

    f = open("%s/%s.svg" % (output_path, dc.country), "w")
    f.write(template_xml.encode("utf-8"))
    f.close()

def main(*args):

    try:
        recipient_indicators = dataprocessing.load_data("recipient_indicators")
        db_donor_data = dataprocessing.load_data("donor_data")
        db_donor_oda = dataprocessing.load_data("donor_oda")
        db_donation_breakdown = dataprocessing.load_data("donation_breakdown")
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
            dc = DonorCountry(country, db_donor_data, db_donor_oda, db_donation_breakdown)
            process_donor_country(dc)
        except ProcessingException, e:
            print "Skipping %s due to processing exception: %s" % (country, e.message)

if __name__ == "__main__":
    main(*sys.argv)
