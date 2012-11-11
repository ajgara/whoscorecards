import csv
import models
import ftypes

def strip_perc(s):
    return models.SafeFloat(s.replace("%", ""))

def parse_disbursements(fp):
    transforms = {
        "Donor" : str,
        "Year" : str,
        "OTHER ODA" : models.SafeFloat,
        "Total Health" : models.SafeFloat,
        "Total ODA" : models.SafeFloat,
        "%age" : strip_perc,
    }
    
    reader = csv.reader(fp)
    headers = reader.next()
    rows = [headers] 
    for row in reader:
        values = [transforms[k](v) for (k, v) in zip(headers, row)]
        rows.append(values)
    return ftypes.list(*rows) / (lambda x : x.Year == "2010")

if __name__ == "__main__":
    parse_disbursements(open("../../../data/Table1 Chart2.csv"))
