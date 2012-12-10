import csv
import os
from django.conf import settings
import models
import ftypes


path_to_file = lambda x : os.path.join(settings.DATA_ROOT, x)
data_files = {
    "disbursements" : path_to_file("Table1 Chart2.csv"),
    "purpose_commitments" : path_to_file("Table 3&5 Chart 4&6.csv"),
    "purpose_disbursements" : path_to_file("Table 3&5 Chart 4&6_d.csv"),
    "disbursement_by_income" : path_to_file("Table 7 Chart 8.csv"),
    "disbursement_by_region" : path_to_file("Table 9 Chart 10.csv"),
    "disbursement_by_country" : path_to_file("Table13 Chart14.csv"),
    "recipient_countries" : path_to_file("Chart14.csv"),
}

def strip_perc(s):
    return models.SafeFloat(s.replace("%", ""))

def parse_file(fp, transforms):
    reader = csv.reader(fp)
    headers = reader.next()
    rows = [headers] 
    for row in reader:
        values = [transforms[k](v) for (k, v) in zip(headers, row)]
        rows.append(values)
    return ftypes.list(*rows)

def parse_disbursements(fp):
    transforms = {
        "Donor" : str,
        "Year" : str,
        "OTHER ODA" : models.SafeFloat,
        "Total Health" : models.SafeFloat,
        "Total ODA" : models.SafeFloat,
        "%age" : strip_perc,
    }
    return parse_file(fp, transforms)
    

def parse_purpose_commitments(fp):
    transforms = {
        "Donor" : str,
        "Year" : str,
        "Purpose" : str,
        "Commitments, Million, constant 2009 US$" : models.SafeFloat,
    }
    return parse_file(fp, transforms)

def parse_purpose_disbursements(fp):
    transforms = {
        "Donor" : str,
        "Year" : str,
        "Purpose" : str,
        "Disbursements, Million, constant 2009 US$" : models.SafeFloat,
    }
    return parse_file(fp, transforms)

def parse_disbursement_by_income(fp):
    transforms = {
        "Donor" : str,
        "Year" : str,
        "Income Group" : str,
        "Disbursements, Million, constant 2009 US$" : models.SafeFloat,

    }
    return parse_file(fp, transforms)

def parse_disbursement_by_region(fp):
    transforms = {
        "Donor" : str,
        "Year" : str,
        "WHO Region" : str,
        "Disbursements, Million, constant 2009 US$" : models.SafeFloat,

    }
    return parse_file(fp, transforms)

def parse_disbursements_by_country(fp):
    transforms = {
        "Donor" : str,
        "ISO3" : str,
        "Recipient" : str,
        "Economic Development" : str,
        "WHO Region" : str,
        "HEALTH POLICY & ADMIN. MANAGEMENT" : models.SafeFloat,
        "MDG6" : models.SafeFloat,
        "Other Health Purposes" : models.SafeFloat,
        "RH & FP" : models.SafeFloat,
        "Disbursements, Million, 2009 constant US$ \nTotal" : models.SafeFloat,
    }
    return parse_file(fp, transforms)

def parse_recipient_countries(fp):
    transforms = {
        "Donor" : str,
        "ISO3" : str,
        "Recipient" : str,
        "HEALTH POLICY & ADMIN. MANAGEMENT" : models.SafeFloat,
        "MDG6" : models.SafeFloat,
        "Other Health Purposes" : models.SafeFloat,
        "RH & FP" : models.SafeFloat,
        "Disbursements, Million, 2009 constant US$ \nTotal" : models.SafeFloat,
        "Ordinal" : int,
        "Percentage" : strip_perc,
    }
    return parse_file(fp, transforms)
    

if __name__ == "__main__":
    #parse_disbursements(open("../../../data/Table1 Chart2.csv"))
    #print parse_purpose(open("../../../data/Table 3&5 Chart 4&6.csv"))
    print parse_disbursement_by_income(open(data_files["disbursement_by_income"]))
    #print parse_disbursement_by_region(open("../../../data/Table 9 Chart 10.csv"))
