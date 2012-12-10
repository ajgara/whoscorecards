from django.http import HttpResponse
import json
import parsers
import ftypes
import locale

# TODO not sure if this is the right thing to do
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

def round2(x):
    return locale.format("%.2f", x, grouping=True)

def extract(field):
    return lambda x : x[field]

def filter_by(field, value):
    return lambda x : x[field] == value

def filter_and_extract(data, filter_by, extract):
    return (data / filter_by) * extract

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
    return [year_map.get(str(year), None) for year in years]

def foz(x):
    try:
        return float(x)
    except:
        return 0

def fod(x):
    try:
        return round2(float(x))
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
    def recipient_countries(self):
        filename = parsers.data_files["recipient_countries"]
        data = parsers.parse_recipient_countries(open(filename)) / extract_donor(self.donor)
        data /= extract_donor(self.donor)
        return data

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
    recipient_countries = sorted(donordata.recipient_countries, key=lambda x: x["Ordinal"])

    value_field = "Disbursements, Million, 2009 constant US$ \nTotal"
    by_country_top_40 = sorted(by_country, key=lambda x: x[value_field], reverse=True)[0:40]

    extract_purpose = lambda x : [x[purpose] for purpose in purpose_categories]    

    data = {
        "country_name" : donor,
        "by_country_table" : [
            [ [row["Recipient"]] for row in by_country_top_40 ],
            [ [row["Economic Development"]] for row in by_country_top_40 ],
            [ [row["WHO Region"]] for row in by_country_top_40 ],
            [ [fod(row["HEALTH POLICY & ADMIN. MANAGEMENT"])] for row in by_country_top_40 ],
            [ [fod(row["MDG6"])] for row in by_country_top_40 ],
            [ [fod(row["Other Health Purposes"])] for row in by_country_top_40 ],
            [ [fod(row["RH & FP"])] for row in by_country_top_40 ],
            [ [fod(row[value_field])] for row in by_country_top_40 ]
        ],
        "recipient_pies" : [
            map(foz, extract_purpose(rc)) for rc in recipient_countries
        ],
        "recipient_percs" : [
            round2(rc["Percentage"]) for rc in recipient_countries
        ],
        "recipient_countries" : [
            rc["Recipient"] for rc in recipient_countries
        ],
    }
    js = json.dumps(data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_page1(request, donor=None):
    donordata = DonorData(donor)

    # disbursements
    disbursements = donordata.disbursements
    total_disbursements = disbursements * extract("Total ODA")
    other_disbursements = disbursements * extract("OTHER ODA")
    total_health_disbursements = disbursements * extract("Total Health")
    oda_percentage = disbursements * extract("%age")

    # allocation - commitments
    commitments = donordata.purpose_commitments
    c_policy, c_mdg6, c_other, c_rhfp = commitments
    c_pies = zip(*commitments)
    c_bar = [sum(foz(el) for el in year) for year in c_pies]

    # allocation - disbursements
    disbursements = donordata.purpose_disbursements
    d_policy, d_mdg6, d_other, d_rhfp = disbursements
    d_pies = zip(*disbursements)
    d_bar = [sum(foz(el) for el in year) for year in d_pies]

    # disbursement by income
    by_income = donordata.disbursement_by_income
    get_disbursement = extract("Disbursements, Million, constant 2009 US$")
    filter_and_extract_income = lambda x : filter_and_extract(
        by_income, filter_by("Income Group", x), get_disbursement
    )
    ldcs = filter_and_extract_income("LDCs")
    lics = filter_and_extract_income("Other LICs")
    lmics = filter_and_extract_income("LMICs")
    umics = filter_and_extract_income("UMICs")
    gmc = filter_and_extract_income("Global and multi-country")

    # disbursement by region
    by_region = donordata.disbursement_by_region
    get_disbursement = extract("Disbursements, Million, constant 2009 US$")
    filter_and_extract_income = lambda x : filter_and_extract(
        by_region, filter_by("WHO Region", x), get_disbursement
    )
    afr = filter_and_extract_income("Afr")
    amr = filter_and_extract_income("Amr")
    emr = filter_and_extract_income("Emr")
    eur = filter_and_extract_income("Eur")
    sear = filter_and_extract_income("Sear")
    multicount = filter_and_extract_income("Multicount")
    not_un = filter_and_extract_income("Not UN")
    
    by_income_domain_y = [0, max(ldcs + lics + lmics + umics + gmc)*1.2]
    by_region_domain_y = [0, max(afr + amr + emr + eur + sear + multicount + not_un)*1.2]
    domain_x = range(2000, 2011)

    data = {
        "country_name" : donor,
        "disbursements_table" : [
            total_disbursements * round2, total_health_disbursements * round2, oda_percentage * round2
        ],
        "disbursements_graph" : {
            "other" : {
                "data" : other_disbursements,
                "data-labels" : [round2(item) for item in other_disbursements],
                "domain-y" : [ 0, max(total_disbursements)*1.2 ],
                "labels" : domain_x
            },
            "health" : {
                "data" : total_health_disbursements,
                "data-labels" : [round2(item) for item in total_health_disbursements],
                "domain-y" : [ 0, max(total_disbursements)*1.2 ],
                "labels" : domain_x
            }
        },
        

        # Commitments
        "purpose_commitments_table" : [
            map(fod, c_policy), map(fod, c_mdg6), map(fod, c_other), map(fod, c_rhfp)
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
        "health_total_commitments_bar" : {
                "data" : c_bar,
                "data-labels" : map(round2, c_bar),
                "domain-y" : [0, max(c_bar)*1.2],
                "labels" : domain_x
            },

        "arrow_commitments" : c_bar[10] - c_bar[9],
        "arrow_commitments_text" : round2(c_bar[10] - c_bar[9]),

        # Disbursements
        "purpose_disbursements_table" : [
            map(fod, d_policy), map(fod, d_mdg6), map(fod, d_other), map(fod, d_rhfp)
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
        "health_total_disbursements_bar" : {
                "data" : d_bar,
                "data-labels" : map(round2, d_bar),
                "domain-y" : [0, max(d_bar)*1.2],
                "labels" : domain_x
            },

        "arrow_disbursements" : d_bar[10] - d_bar[9],
        "arrow_disbursements_text" : round2(d_bar[10] - d_bar[9]),

        # By Income
        "by_income_table" : [
            ldcs * fod, 
            lics * fod, 
            lmics * fod, 
            umics * fod, 
            gmc * fod
        ],
        "by_income_graph" : [
            {
                "data" : ldcs,
                "domain-y" : by_income_domain_y,
                "labels" : domain_x
            },
            {
                "data" : lics,
                "domain-y" : by_income_domain_y,
                "labels" : domain_x
            },
            {
                "data" : lmics,
                "domain-y" : by_income_domain_y,
                "labels" : domain_x
            },
            {
                "data" : umics,
                "domain-y" : by_income_domain_y,
                "labels" : domain_x
            },
            {
                "data" : gmc,
                "domain-y" : by_income_domain_y,
                "labels" : domain_x
            }
        ],

        # By Region
        "by_region_table" : [
           afr * fod, 
           amr * fod,
           emr * fod,
           eur * fod,
           sear * fod,
           multicount * fod,
           not_un * fod
        ],
        "by_region_graph" : [
            {
                "data" : afr,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            },
            {
                "data" : amr,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            },
            {
                "data" : emr,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            },
            {
                "data" : eur,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            },
            {
                "data" : sear,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            },
            {
                "data" : multicount,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            },
            {
                "data" : not_un,
                "domain-y" : by_region_domain_y,
                "labels" : domain_x
            }
        ]
    }

    js = json.dumps(data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")
