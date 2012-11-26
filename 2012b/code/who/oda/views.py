from django.http import HttpResponse
import json
import parsers
import ftypes

def encoder(arg):
    if type(arg) == ftypes.list:
        return list(arg)
    return dict(arg)

class DonorData(object):
    def __init__(self, donor):
        self.donor = donor

    @property
    def disbursements(self):
        filename = parsers.data_files["disbursements"]
        data = parsers.parse_disbursements(open(filename))
        data /= (lambda x : x.Donor == self.donor)
        return data

    @property
    def purpose(self):
        filename = parsers.data_files["purpose"]
        data = parsers.parse_purpose(open(filename))
        data /= (lambda x : x.Donor == self.donor)
        return data

    @property
    def disbursement_by_income(self):
        filename = parsers.data_files["disbursement_by_income"]
        data = parsers.parse_disbursement_by_income(open(filename))
        data /= (lambda x : x.Donor == self.donor)
        return data

    @property
    def disbursement_by_region(self):
        filename = parsers.data_files["disbursement_by_region"]
        data = parsers.parse_disbursement_by_region(open(filename))
        data /= (lambda x : x.Donor == self.donor)
        return data

def json_disbursements(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.disbursements, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_purpose(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.purpose, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_disbursement_by_income(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.disbursement_by_income, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_disbursement_by_region(request, donor=None):
    donordata = DonorData(donor)
    js = json.dumps(donordata.disbursement_by_region, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_page1(request, donor=None):
    def extract(field):
        return lambda x : x[field]

    def filter_by(field, value):
        return lambda x : x[field] == value

    def filter_and_extract(data, filter_by, extract):
        return list(data / filter_by * extract)
    
    donordata = DonorData(donor)

    # disbursements
    disbursements = donordata.disbursements
    total_disbursements = disbursements * (lambda x : x["Total ODA"])
    total_health_disbursements = disbursements * (lambda x : x["Total Health"])
    oda_percentage = disbursements * (lambda x : x["%age"])

    # allocation - commitments
    commitments = donordata.purpose

    get_commitment = extract("Commitments, Million, constant 2009 US$")

    filter_and_extract_commitments = lambda x : filter_and_extract(
        commitments, filter_by("Purpose", x), get_commitment
    )

    c_policy = filter_and_extract_commitments("HEALTH POLICY & ADMIN. MANAGEMENT")
    c_mdg6 = filter_and_extract_commitments("MDG6")
    c_other = filter_and_extract_commitments("Other Health Purposes")
    c_rhfp = filter_and_extract_commitments("RH & FP")
    c_pies = zip(c_policy, c_mdg6, c_other, c_rhfp)

    c_bar = [sum(el for el in year if el) for year in c_pies]

    # allocation - disbursements
    # TODO fix this - this is actually commitments
    disbursements = donordata.purpose
    # TODO fix this - this is actually commitments
    get_disbursement = extract("Commitments, Million, constant 2009 US$")
    filter_and_extract_disbursements = lambda x : filter_and_extract(
        disbursements, filter_by("Purpose", x), get_disbursement
    )
    d_policy = filter_and_extract_disbursements("HEALTH POLICY & ADMIN. MANAGEMENT")
    d_mdg6 = filter_and_extract_disbursements("MDG6")
    d_other = filter_and_extract_disbursements("Other Health Purposes")
    d_rhfp = filter_and_extract_disbursements("RH & FP")
    d_pies = zip(d_policy, d_mdg6, d_other, d_rhfp)
    d_bar = total_health_disbursements

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

    data = {
        "country_name" : donor,
        "disbursements_table" : [
            total_disbursements, total_health_disbursements, oda_percentage
        ],
        "purpose_commitments_table" : [
            c_policy, c_mdg6, c_other, c_rhfp
        ],
        # Commitments
        "purpose_commitments_pie_2000" : c_pies[0],
        "purpose_commitments_pie_2001" : c_pies[1],
        "purpose_commitments_pie_2002" : c_pies[2],
        "purpose_commitments_pie_2003" : c_pies[3],
        "purpose_commitments_pie_2004" : c_pies[4],
        "purpose_commitments_pie_2005" : c_pies[5],
        "purpose_commitments_pie_2006" : c_pies[6],
        # TODO This data is missing for the moment
        "purpose_commitments_pie_2007" : c_pies[0],
        "purpose_commitments_pie_2008" : c_pies[0],
        "purpose_commitments_pie_2009" : c_pies[0],
        "purpose_commitments_pie_2010" : c_pies[0],
        "health_total_commitments_bar" : c_bar,

        # Disbursements
        "purpose_disbursements_pie_2000" : d_pies[0],
        "purpose_disbursements_pie_2001" : d_pies[1],
        "purpose_disbursements_pie_2002" : d_pies[2],
        "purpose_disbursements_pie_2003" : d_pies[3],
        "purpose_disbursements_pie_2004" : d_pies[4],
        "purpose_disbursements_pie_2005" : d_pies[5],
        "purpose_disbursements_pie_2006" : d_pies[6],
        # TODO This data is missing for the moment
        "purpose_disbursements_pie_2007" : d_pies[0],
        "purpose_disbursements_pie_2008" : d_pies[0],
        "purpose_disbursements_pie_2009" : d_pies[0],
        "purpose_disbursements_pie_2010" : d_pies[0],
        "health_total_disbursements_bar" : d_bar,

        # By Income
        "by_income_table" : [
            ldcs, lics, lmics, umics, gmc
        ],
    }

    js = json.dumps(data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")
