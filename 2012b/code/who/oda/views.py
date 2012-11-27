from django.http import HttpResponse
import json
import parsers
import ftypes

def round2(x):
    return round(x, 2)

def extract(field):
    return lambda x : x[field]

def filter_by(field, value):
    return lambda x : x[field] == value

def filter_and_extract(data, filter_by, extract):
    return list(data / filter_by * extract)

def extract_donor(donor):
    return lambda x : x.Donor == donor

def encoder(arg):
    if type(arg) == ftypes.list:
        return list(arg)
    return dict(arg)

def extract_year_data(value_field):
    return lambda x : (x["Year"], x[value_field])

def align_years(data, years=range(2000, 2011)):
    year_map = dict(data)
    val_or_dash = lambda x : x if x else "-"
    return [fod(year_map.get(str(year), None)) for year in years]

def foz(x):
    try:
        return float(x)
    except:
        return 0

def fod(x):
    try:
        return float(x)
    except:
        return "-"

def sum_ignore_nones(arr):
    return sum(foz(x) for x in arr)

purpose_categories = [
    "HEALTH POLICY & ADMIN. MANAGEMENT",
    "MDG6",
    "Other Health Purposes",
    "RH & FP",
]

class DonorData(object):
    def __init__(self, donor):
        self.donor = donor

    @property
    def disbursements(self):
        filename = parsers.data_files["disbursements"]
        data = parsers.parse_disbursements(open(filename)) / extract_donor(self.donor)
        data /= extract_donor(self.donor)
        return data

    @property
    def purpose_commitments(self):
        filename = parsers.data_files["purpose_commitments"]
        data = parsers.parse_purpose_commitments(open(filename))
        data /= extract_donor(self.donor)

        value_field = "Commitments, Million, constant 2009 US$"
        output = [
            align_years(                            # Fill in missing data gaps
                filter_and_extract(
                    data, 
                    filter_by("Purpose", category), # Filter a specific purpose category
                    extract_year_data(value_field)  # Extract an array of (year, data) tuples
                )
            )
            for category in purpose_categories
        ]
        return output

    @property
    def purpose_disbursements(self):
        filename = parsers.data_files["purpose_disbursements"]
        data = parsers.parse_purpose_disbursements(open(filename))
        data /= extract_donor(self.donor)

        value_field = "Disbursements, Million, constant 2009 US$"
        output = [
            align_years(                            # Fill in missing data gaps
                filter_and_extract(
                    data, 
                    filter_by("Purpose", category), # Filter a specific purpose category
                    extract_year_data(value_field)  # Extract an array of (year, data) tuples
                )
            )
            for category in purpose_categories
        ]
        return output

    @property
    def disbursement_by_income(self):
        filename = parsers.data_files["disbursement_by_income"]
        data = parsers.parse_disbursement_by_income(open(filename))
        data /= extract_donor(self.donor)
        return data

    @property
    def disbursement_by_region(self):
        filename = parsers.data_files["disbursement_by_region"]
        data = parsers.parse_disbursement_by_region(open(filename))
        data /= extract_donor(self.donor)
        return data

    @property
    def disbursement_by_country(self):
        filename = parsers.data_files["disbursement_by_country"]
        data = parsers.parse_disbursements_by_country(open(filename))
        data /= extract_donor(self.donor)
        return data

def json_disbursements(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.disbursements, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_purpose_commitments(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.purpose_commitments, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_purpose_disbursements(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.purpose_disbursements, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_disbursement_by_income(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.disbursement_by_income, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_disbursement_by_region(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.disbursement_by_region, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_page2(request, donor=None):
    donordata = DonorData(donor)

    by_country = donordata.disbursement_by_country
    value_field = "Disbursements, Million, 2009 constant US$ \nTotal"
    by_country_top_30 = sorted(by_country, key=lambda x: x[value_field], reverse=True)[0:30]
    by_country_without_global = sorted(
        by_country / (lambda x: x["Recipient"] != "Global and Regional"),
        key = lambda x: x[value_field],
        reverse=True
    )

    extract_purpose = lambda x : [x[purpose] for purpose in purpose_categories]  # extract purpose data   
    extract_purpose = lambda x : [x[purpose] for purpose in purpose_categories]    
    global_pie = filter_and_extract(
        by_country, 
        lambda x: x["Recipient"] == "Global and Regional",         # filter Global
        extract_purpose
    )[0]

    top8_pies = [
        extract_purpose(el)
        for el in by_country_without_global[0:8]
    ]

    total_oda = sum_ignore_nones([
        el[value_field] for el in by_country
    ])
    print top8_pies
    other_oda = (total_oda - sum_ignore_nones(global_pie) - sum([sum_ignore_nones(pie) for pie in top8_pies])) / total_oda
    

    top8_countries = [
        el["Recipient"]
        for el in by_country_without_global[0:8]
    ]
    

    data = {
        "by_country_table" : [
            [
                row["Recipient"],
                row["Economic Development"],
                row["WHO Region"],
                fod(row["HEALTH POLICY & ADMIN. MANAGEMENT"]),
                fod(row["MDG6"]),
                fod(row["Other Health Purposes"]),
                fod(row["RH & FP"]),
                fod(row[value_field]),
            ]
            for row in by_country_top_30
        ],
        "recipient_pies" : [
            map(foz, global_pie), 
            map(foz, top8_pies[0]),
            map(foz, top8_pies[1]),
            map(foz, top8_pies[2]),
            map(foz, top8_pies[3]),
            map(foz, top8_pies[4]),
            map(foz, top8_pies[5]),
            map(foz, top8_pies[6]),
            map(foz, top8_pies[7]),
        ],
        "recipient_percs" : [
            round2(sum_ignore_nones(global_pie) / total_oda),
            round2(sum_ignore_nones(top8_pies[0]) / total_oda),
            round2(sum_ignore_nones(top8_pies[1]) / total_oda),
            round2(sum_ignore_nones(top8_pies[2]) / total_oda),
            round2(sum_ignore_nones(top8_pies[3]) / total_oda),
            round2(sum_ignore_nones(top8_pies[4]) / total_oda),
            round2(sum_ignore_nones(top8_pies[5]) / total_oda),
            round2(sum_ignore_nones(top8_pies[6]) / total_oda),
            round2(sum_ignore_nones(top8_pies[7]) / total_oda),
            round2(other_oda),
        ],
        "recipient_countries" : [
            "Global and Regional",
            top8_countries[0],
            top8_countries[1],
            top8_countries[2],
            top8_countries[3],
            top8_countries[4],
            top8_countries[5],
            top8_countries[6],
            top8_countries[7],
        ]
    }
    js = json.dumps(data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_page1(request, donor=None):
    donordata = DonorData(donor)

    # disbursements
    disbursements = donordata.disbursements
    total_disbursements = disbursements * (lambda x : x["Total ODA"])
    total_health_disbursements = disbursements * (lambda x : x["Total Health"])
    oda_percentage = disbursements * (lambda x : x["%age"])

    # allocation - commitments
    commitments = donordata.purpose_commitments
    c_policy, c_mdg6, c_other, c_rhfp = commitments
    c_pies = zip(*commitments)
    c_bar = [round2(sum([foz(el) for el in year])) for year in c_pies]

    # allocation - disbursements
    disbursements = donordata.purpose_disbursements
    d_policy, d_mdg6, d_other, d_rhfp = disbursements
    d_pies = zip(*disbursements)
    d_bar = [round2(sum([foz(el) for el in year])) for year in d_pies]

    # disbursement by income
    by_income = donordata.disbursement_by_income
    get_disbursement = extract("Disbursements, Million, constant 2009 US$")
    filter_and_extract_income = lambda x : filter_and_extract(
        by_income, filter_by("Income Group", x), get_disbursement
    )
    ldcs = map(fod, filter_and_extract_income("LDCs"))
    lics = map(fod, filter_and_extract_income("Other LICs"))
    lmics = map(fod, filter_and_extract_income("LMICs")) 
    umics = map(fod, filter_and_extract_income("UMICs"))
    gmc = map(fod, filter_and_extract_income("Global and multi-country"))

    # disbursement by region
    by_region = donordata.disbursement_by_region
    get_disbursement = extract("Disbursements, Million, constant 2009 US$")
    filter_and_extract_income = lambda x : filter_and_extract(
        by_region, filter_by("WHO Region", x), get_disbursement
    )
    afr = map(fod, filter_and_extract_income("Afr")) 
    amr = map(fod, filter_and_extract_income("Amr")) 
    emr = map(fod, filter_and_extract_income("Emr")) 
    eur = map(fod, filter_and_extract_income("Eur")) 
    sear = map(fod, filter_and_extract_income("Sear")) 
    multicount = map(fod, filter_and_extract_income("Multicount"))
    not_un = map(fod, filter_and_extract_income("Not UN"))
    
    by_income_domain_y = [ 0, max(ldcs + lics + lmics + umics + gmc) ]
    by_region_domain_y = [ 0, max(afr + amr + emr + eur + sear + multicount + not_un) ]

    data = {
        "country_name" : donor,
        "disbursements_table" : [
            total_disbursements, total_health_disbursements, oda_percentage
        ],
        "disbursements_graph" : {
            "total" : {
                "data" : total_disbursements,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            "health" : {
                "data" : total_health_disbursements,
                "domain-y" : [ 0, max(total_disbursements) ],
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            }
        },
        

        # Commitments
        "purpose_commitments_table" : [
            c_policy, c_mdg6, c_other, c_rhfp
        ],
        "purpose_commitments_pie_2000" : map(foz, c_pies[0]),
        "purpose_commitments_pie_2001" : map(foz, c_pies[1]),
        "purpose_commitments_pie_2002" : map(foz, c_pies[2]),
        "purpose_commitments_pie_2003" : map(foz, c_pies[3]),
        "purpose_commitments_pie_2004" : map(foz, c_pies[4]),
        "purpose_commitments_pie_2005" : map(foz, c_pies[5]),
        "purpose_commitments_pie_2006" : map(foz, c_pies[6]),
        "purpose_commitments_pie_2007" : map(foz, c_pies[7]),
        "purpose_commitments_pie_2008" : map(foz, c_pies[8]),
        "purpose_commitments_pie_2009" : map(foz, c_pies[9]),
        "purpose_commitments_pie_2010" : map(foz, c_pies[10]),
        "health_total_commitments_bar" : c_bar,

        "arrow_commitments" : c_bar[10] - c_bar[9],
        "arrow_commitments_text" : round2(c_bar[10] - c_bar[9]),

        # Disbursements
        "purpose_disbursements_table" : [
            d_policy, d_mdg6, d_other, d_rhfp
        ],
        "purpose_disbursements_pie_2000" : map(foz, d_pies[0]),
        "purpose_disbursements_pie_2001" : map(foz, d_pies[1]),
        "purpose_disbursements_pie_2002" : map(foz, d_pies[2]),
        "purpose_disbursements_pie_2003" : map(foz, d_pies[3]),
        "purpose_disbursements_pie_2004" : map(foz, d_pies[4]),
        "purpose_disbursements_pie_2005" : map(foz, d_pies[5]),
        "purpose_disbursements_pie_2006" : map(foz, d_pies[6]),
        "purpose_disbursements_pie_2007" : map(foz, d_pies[7]),
        "purpose_disbursements_pie_2008" : map(foz, d_pies[8]),
        "purpose_disbursements_pie_2009" : map(foz, d_pies[9]),
        "purpose_disbursements_pie_2010" : map(foz, d_pies[10]),
        "health_total_disbursements_bar" : d_bar,

        "arrow_disbursements" : d_bar[10] - d_bar[9],
        "arrow_disbursements_text" : round2(d_bar[10] - d_bar[9]),

        # By Income
        "by_income_table" : [
            ldcs, lics, lmics, umics, gmc
        ],
        "by_income_graph" : [
            {
                "data" : ldcs,
                "domain-y" : by_income_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : lics,
                "domain-y" : by_income_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : lmics,
                "domain-y" : by_income_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : umics,
                "domain-y" : by_income_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : gmc,
                "domain-y" : by_income_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            }
        ],

        # By Region
        "by_region_table" : [
            afr, amr, emr, eur, sear, multicount, not_un
        ],
        "by_region_graph" : [
            {
                "data" : afr,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : amr,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : emr,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : eur,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : sear,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : multicount,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            },
            {
                "data" : not_un,
                "domain-y" : by_region_domain_y,
                "labels" : [ "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010" ]
            }
        ]
    }

    js = json.dumps(data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")
