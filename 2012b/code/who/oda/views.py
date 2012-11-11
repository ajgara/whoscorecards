from django.http import HttpResponse
import json
import parsers

def encoder(arg):
    return dict(arg)

def json_disbursements(request, donor=None):
    filename = parsers.data_files["disbursements"]
    data = parsers.parse_disbursements(open(filename))
    data /= (lambda x : x.Donor == donor)
    js = json.dumps(data.data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_purpose(request, donor=None):
    filename = parsers.data_files["purpose"]
    data = parsers.parse_purpose(open(filename))
    data /= (lambda x : x.Donor == donor)
    js = json.dumps(data.data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_disbursement_by_income(request, donor=None):
    filename = parsers.data_files["disbursement_by_income"]
    data = parsers.parse_disbursement_by_income(open(filename))
    data /= (lambda x : x.Donor == donor)
    js = json.dumps(data.data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

def json_disbursement_by_region(request, donor=None):
    filename = parsers.data_files["disbursement_by_region"]
    data = parsers.parse_disbursement_by_region(open(filename))
    data /= (lambda x : x.Donor == donor)
    js = json.dumps(data.data, indent=4, default=encoder)
    return HttpResponse(js, mimetype="application/json")

