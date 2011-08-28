import numbers
from xml.dom import minidom
import os
import math
import sys
import xlrd
import ftypes
from pivottable import PivotTable, GroupBy, Sum
import dataprocessing
import processutils
from processutils import process_svg_template, none_is_zero, fmt_pop, fmt_1000, fmt_perc, fmt_r0, fmt_r1, fmt_r2

recipient_svg = "../svg/WHO_ODA_recipient.svg"
output_path = "gen_recipients"

recipient_indicators = None
sources_data = None

is_country = lambda country : lambda x : x.ISO3 == country 

class ProcessingException(Exception):
    pass

class RecipientCountry(object):
    def __init__(self, iso3, recipient_indicators, donor_data):
        self._recipient_indicators = recipient_indicators.data / is_country(iso3)
        self._donor_data = donor_data.data / is_country(iso3)
        if len(self._recipient_indicators) == 0:
            raise ProcessingException("Could not find data for %s" % iso3)
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
    def donations(self):
        pt = PivotTable()
        pt.xaxis = "MDG Purpose"
        pt.yaxis = [
            {"attr" : "donorname_e", "label" : "country", "aggr" : GroupBy},
            {"attr" : "2007-2009", "label" : "amount", "aggr" : Sum},
        ]
        pt.yaxis_order = ["donorname_e"]
        pt.rows = self._donor_data
        table = ftypes.list(*[a for a in pt.result])
        return table

    def __getattr__(self, attr_key):
        if attr_key in self.colmap:
            data_key = self.colmap[attr_key]

            coldata = self._recipient_indicators.__getattr__(data_key)
            return self._yearzip(coldata)
        elif attr_key in ["mdg6_perc", "rhfp_perc", "other_health_perc", "unspecified_perc"]:
            new_key = attr_key.replace("_perc", "")
            num_arr = self.__getattr__(new_key)
            den_arr = self.__getattr__("oda_health")
            return { year : numutils.safediv(num_arr[year], den_arr[year]) for year in num_arr.keys()}
        else:
            return object.__getattribute__(self, attr_key)

class numutils(object):
    @staticmethod
    def condround(val):
        if val < 0.1:
            return val
        elif val < 1:
            return round(val, 1)
        elif val < 100:
            return round(val)
        else:
            return round(val, -1)
    @staticmethod
    def safediv(num, den):
        if not isinstance(num, numbers.Number) or not isinstance(den, numbers.Number):
            return 0
        if den == 0:
            return 0.0
        else:
            return num / den

class xmlutils(object):
    @staticmethod
    def get_el_by_id(dom, elname, id):
        elements = dom.getElementsByTagName(elname)
        match = [el for el in elements if el.attributes["id"].value == id]
        return None if len(match) == 0 else match[0]

class BarGraph(object):
    def __init__(self, tick_multiplier=1.2, num_ticks=6, min_height=285.5, max_height=223):
        self.values = {}
        self.max_height = max_height
        self.min_height = min_height
        self.num_ticks = num_ticks
        self.tick_multiplier = tick_multiplier

    def add_value(self, year, value):
        self.values[int(year)] = value

    @property
    def ticks(self):
        high = max(self.values.values())
        top = numutils.condround(high * self.tick_multiplier)
        ticksz = top / (self.num_ticks - 1)
        return { tick + 1 : ticksz * tick for tick in range(self.num_ticks) }

    @property
    def max_tick(self):
        return self.ticks[self.num_ticks]

    @property
    def pixel_range(self):
        return abs(self.max_height - self.min_height)

    def update_bars(self, xml, ids):
        for year in range(2002, 2010):
            node = xmlutils.get_el_by_id(xml, "path", ids[year])
            d = node.attributes["d"].value.split()
            d[2] = "V"
            d[3] = str(self.min_height - self.values[year] / self.max_tick * self.pixel_range)
            node.attributes["d"].value = " ".join(d)

    def update_values(self, xml, ids):
        for year in range(2002, 2010):
            node = xmlutils.get_el_by_id(xml, "text", ids[year])
            height = self.min_height - self.values[year] / self.max_tick * self.pixel_range
            node.setAttribute("y", str(height - 6))

def cleanup():
    sys.exit()

def process_expenditure_table(recipient_country, template_xml):

    rc = recipient_country
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
    template_xml = process_svg_template(data, template_xml)
    return template_xml

def process_donor_table(recipient_country, template_xml):
    rc = recipient_country
    data = {}

    donations = rc.donations
    def country_donations(donor_country):
        return donations / (lambda x : x["donorname_e"] == donor_country)
    def data_mdg6(donor_country):
        donor_data = country_donations(donor_country)
        if donor_data == None or len(donor_data) == 0: return 0
        return none_is_zero(donor_data[0].get("MDG6", None))
    def data_rhfp(donor_country):
        donor_data = country_donations(donor_country)
        if donor_data == None or len(donor_data) == 0: return 0
        return none_is_zero(donor_data[0].get("RH & FP", None))
    def data_other(donor_country):
        donor_data = country_donations(donor_country)
        if donor_data == None or len(donor_data) == 0: return 0
        return none_is_zero(donor_data[0].get("Other Health Purposes", None))
    def data_unspecified(donor_country):
        donor_data = country_donations(donor_country)
        if donor_data == None or len(donor_data) == 0: return 0
        return none_is_zero(donor_data[0].get("Unallocated", None))

    for abbr, donor_country in [
        ("aus", "Australia"), ("ast", "Austria"), ("bel", "Belgium"), ("can", "Canada"), 
        ("den", "Denmark"), ("fin", "Finland"), ("fra", "France"), ("ger", "Germany"), 
        ("gre", "Greece"), ("ire", "Ireland"), ("ita", "Italy"), ("jap", "Japan"),
        ("lux", "Luxembourg"), ("net", "Netherlands"), ("nor", "Norway"), ("kor", "Republic of Korea"),
        ("spa", "Spain"), ("swe", "Sweden"), ("uk", "United Kingdom"), ("us", "United States of America"),
        ("ec", "EC"), ("gavi", "GAVI"), ("gf", "GFATM"), ("ida", "IDA"),
        ("una", "UNAIDS"), ("und", "UNDP"), ("unf", "UNFPA"), ("uni", "UNICEF"),
        ]:

        
        mdg6 = data_mdg6(donor_country)
        rf = data_rhfp(donor_country)
        other = data_other(donor_country)
        unspecified = data_unspecified(donor_country)

        data["mdg6_%s" % abbr] = fmt_1000(mdg6)
        data["rf_%s" % abbr] = fmt_1000(rf)
        data["oth_%s" % abbr] = fmt_1000(other)
        data["un_%s" % abbr] = fmt_1000(unspecified)
        data["tot_%s" % abbr] = fmt_1000(mdg6 + rf + other + unspecified)
    template_xml = process_svg_template(data, template_xml)
    return template_xml

def process_health_graph(recipient_country, template_xml):
    rc = recipient_country
    graph = BarGraph(num_ticks=6, min_height=285.5, max_height=223)
    data = {}

    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        data["g1_v%s" % y] = fmt_r1(rc.oda_health[year])
        graph.add_value(year, rc.oda_health[year])

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
    g1_change = rc.oda_health["2009"] - rc.oda_health["2008"]
    data["g1_diff"] = fmt_r1(g1_change)

    perc_2008 = numutils.safediv(rc.oda_health["2008"], rc.oda_commitments["2008"]) * 100
    perc_2009 = numutils.safediv(rc.oda_health["2009"], rc.oda_commitments["2009"]) * 100
    if perc_2008 > perc_2009:
        data["g1_perc"] = "decreased by %s%%" % fmt_r1(perc_2008 - perc_2009)
    else:
        data["g1_perc"] = "increased by %s%%" % fmt_r1(perc_2009 - perc_2008)

    template_xml = process_svg_template(data, template_xml)

    xml = minidom.parseString(template_xml.encode("utf-8"))
    graph.update_bars(xml, {
        2002 : "path22512",
        2003 : "path22522",
        2004 : "path22532",
        2005 : "path22542",
        2006 : "path22552",
        2007 : "path22562",
        2008 : "path22572",
        2009 : "path22582",
    })

    graph.update_values(xml, {
        2002 : "g1_v2",
        2003 : "g1_v3",
        2004 : "g1_v4",
        2005 : "g1_v5",
        2006 : "g1_v6",
        2007 : "g1_v7",
        2008 : "g1_v8",
        2009 : "g1_v9",
    })

    arrow = xmlutils.get_el_by_id(xml, "polygon", "g1_arrow")
    if g1_change < 0:
        arrow.setAttribute("transform", "matrix(-1,0,0,-1,529.8,494)")
        arrow.setAttribute("style", "fill:#be1e2d")

    return xml.toxml()

def process_health_per_capita_graph(recipient_country, template_xml):
    rc = recipient_country
    data = {}
    graph = BarGraph(num_ticks=4, min_height=285.5, max_height=223)
    for year in range(2002, 2010):
        y = str(year)[3]
        year = str(year)
        data["g2_v%s" % y] = fmt_r1(rc.oda_health_per_capita[year])
        graph.add_value(year, rc.oda_health_per_capita[year])

    has_data = isinstance(max(graph.values.values()), numbers.Number)
    if not has_data:
        # No data available for this graph
        return template_xml

    g2_ticks = graph.ticks
    data["g2_t1"] = fmt_r0(g2_ticks[1])
    data["g2_t2"] = fmt_r0(g2_ticks[2])
    data["g2_t3"] = fmt_r0(g2_ticks[3])
    data["g2_t4"] = fmt_r0(g2_ticks[4])

    g2_change = rc.oda_health_per_capita["2009"] - rc.oda_health_per_capita["2008"]
    data["g2_diff"] = fmt_r1(g2_change)

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

    graph.update_values(xml, {
        2002 : "g2_v2",
        2003 : "g2_v3",
        2004 : "g2_v4",
        2005 : "g2_v5",
        2006 : "g2_v6",
        2007 : "g2_v7",
        2008 : "g2_v8",
        2009 : "g2_v9",
    })

    arrow = xmlutils.get_el_by_id(xml, "polygon", "g2_arrow")
    if g2_change < 0:
        arrow.setAttribute("transform", "matrix(-1,0,0,-1,529.8,494)")
        arrow.setAttribute("style", "fill:#be1e2d")
    return xml.toxml()

class PieChart(object):
    def __init__(self, xml, centre, radius, data, colours=None):
        self.xml = xml
        self.centre = centre
        self.radius = radius
        self.data = data
        if colours == None:
            self.colours = ["#cf3d96", "#62a73b", "#79317f", "#009983"]
        else:
            self.colours = colours

    def generate_xml(self):
        total = sum(self.data)
        if total == 0: return

        centre_x, centre_y = self.centre
        percs = [v / total for v in self.data]

        prev_angle = 0
        for perc in percs:
            new_angle = prev_angle + 2 * math.pi * perc
            segment = {
                "centre_x" : centre_x,
                "centre_y" : centre_y,
                "start_x" : centre_x - math.cos(prev_angle) * self.radius,
                "start_y" : centre_y - math.sin(prev_angle) * self.radius,
                "end_x" : centre_x - math.cos(new_angle) * self.radius,
                "end_y" : centre_y - math.sin(new_angle) * self.radius,
                "long_arc" : 1 if perc > 0.5 else 0,
                "radius" : self.radius,
            } 
            self.generate_segment(segment)
            prev_angle = new_angle

    def generate_segment(self, segment):
        colour = self.colours[0]
        self.colours = self.colours[1:] + [colour]
        root = self.xml.documentElement
        segment_node = self.xml.createElement("path")
        path_d="M%(centre_x)f,%(centre_y)f L%(start_x)f,%(start_y)f A%(radius)f, %(radius)f 0 %(long_arc)d,1 %(end_x)f,%(end_y)f Z" % segment
        segment_node.setAttribute("d", path_d)
        segment_node.setAttribute("stoke", "black")
        segment_node.setAttribute("stoke-width", "2")
        segment_node.setAttribute("style", "fill:%s" % colour)
        root.appendChild(segment_node)

def process_allocation_piecharts(recipient_country, template_xml):
    rc = recipient_country
    xml = minidom.parseString(template_xml.encode("utf-8"))
    circle_y = 441
    for year, circle_x in [(2002, 237), (2003, 281), (2004, 328), (2005, 373.8), (2006, 420), (2007, 465.77), (2008, 511.71), (2009, 557.77)]:
        year = str(year)
        chart = PieChart(xml, (circle_x, circle_y), 17, [rc.mdg6[year], rc.rhfp[year], rc.other_health[year], rc.unspecified[year]])
        chart.generate_xml()
    return xml.toxml()

def process_largest_donors(recipient_country, template_xml):
    max_size = 5500 # Area of a 100% circle

    niz = none_is_zero
    rc = recipient_country
    data = {}
    donations = rc.donations

    fn_total_donor_health_oda = lambda x : (
        x["donorname_e"],
        niz(x.get("MDG6", 0)) + niz(x.get("RH & FP", 0)) + 
        niz(x.get("Other Health Purposes", 0)) + niz(x.get("Unallocated", 0))
    )
    fn_get_health_oda = lambda (x, y) : y
    fn_sum_oda = lambda donors : sum([fn_get_health_oda(tpl) for tpl in donors])
    fn_calc_area = lambda perc_donated : perc_donated / 100 * max_size
    fn_calc_radius = lambda perc_donated : math.sqrt(fn_calc_area(perc_donated) / math.pi)

    # Total health oda for each donor
    oda = donations * fn_total_donor_health_oda

    total_oda = fn_sum_oda(oda)
    oda = sorted(oda, key=fn_get_health_oda, reverse=True)
    oda_as_perc = [(x, y/total_oda * 100) for (x, y) in oda]

    top5_oda_donors = oda_as_perc[0:5]
    for i, (country_name, perc_donated) in enumerate(top5_oda_donors):
        s_perc_donated = fmt_r0(perc_donated)
        data["d_v%d" % (i + 1)] = "%s (%s%%)" % (country_name, s_perc_donated)
    top5_perc = fn_sum_oda(top5_oda_donors)
    data["d_tot"] = fmt_r0(top5_perc)

    template_xml = process_svg_template(data, template_xml)

    xml = minidom.parseString(template_xml.encode("utf-8"))
    for i, (country_name, perc_donated) in enumerate(top5_oda_donors):
        node = xmlutils.get_el_by_id(xml, "circle", "d_c%d" % (i + 1))
        radius = fn_calc_radius(perc_donated)
        node.setAttribute("r", str(radius))

    return xml.toxml()

def process_recipient_country(country):
    template_xml = open(recipient_svg, "r").read().decode("utf-8")

    rc = recipient_country = RecipientCountry(country, recipient_indicators, sources_data)


    template_xml = process_expenditure_table(rc, template_xml)
    template_xml = process_donor_table(rc, template_xml)
    template_xml = process_health_graph(rc, template_xml)
    template_xml = process_health_per_capita_graph(rc, template_xml)
    template_xml = process_allocation_piecharts(rc, template_xml)
    template_xml = process_largest_donors(rc, template_xml)

    f = open("%s/%s.svg" % (output_path, country), "w")
    f.write(template_xml.encode("utf-8"))
    f.close()


def main(*args):
    global recipient_indicators, sources_data

    try:
        recipient_indicators = dataprocessing.load_data("recipient_indicators")
        sources_data = dataprocessing.load_data("donor_data")
    except dataprocessing.DataProcessingException, e:
        print >> sys.stderr, e.message
        cleanup()

    #for country in open("../data/recipient/recipients"):
    for country in ["ETH"]:
        country = country.strip()
        if country.startswith("#"): continue
        if os.path.exists("%s/%s.svg" % (output_path, country)):
            continue
        print "Processing: %s" % country
        try:
            process_recipient_country(country)
        except ProcessingException, e:
            print "Skipping %s due to processing exception: %s" % (country, e.message)


if __name__ == "__main__":
    main(*sys.argv)
