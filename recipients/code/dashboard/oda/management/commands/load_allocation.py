from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
import db
import oda.models as oda_models
from collections import defaultdict
import sys
from django.db import transaction

def float_or_none(x):
    try:
        return float(x)
    except TypeError:
        return 0

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_allocation <indicator file>")

    
        with transaction.commit_on_success():
            statistics = defaultdict(int, {})
            fn_indicator = args[0]
            purpose_factory = db.PurposeDBFactory(file_path=fn_indicator)

            countries = {}
            not_found_countries = set()
            mdgpurposes = {}
            total = len(purpose_factory.data)
            count = 0
            for row in purpose_factory.data:
                count += 1
                sys.stdout.write("\r%d of %d" % (count, total))
                sys.stdout.flush()
                try:
                    if row.ISO3 in countries:
                        country = countries[row.ISO3]
                    else:
                        country = oda_models.Recipient.objects.get(iso3=row.ISO3)
                        countries[row.ISO3] = country

                    row_mdg = row["MDG Purpose 2010"]
                    if row_mdg in mdgpurposes:
                        mdgpurpose = mdgpurposes[row_mdg]
                    else:
                        mdgpurpose, _ = oda_models.MDGPurpose.objects.get_or_create(name=row_mdg)
                        mdgpurposes[row_mdg] = mdgpurpose

                    oda_models.Allocation.objects.filter(
                        country=country, 
                        mdgpurpose=mdgpurpose,
                        year=row.Year
                    ).delete()

                    #if row.ISO3 == "AFG":
                    #    import pdb; pdb.set_trace()
                    allocation = oda_models.Allocation.objects.create(
                        country=country, 
                        mdgpurpose=mdgpurpose,
                        year=row.Year, 
                        commitment=float_or_none(row["Commitments MUSD"]),
                        disbursement=float_or_none(row["Disbursements"]),
                    )
                except oda_models.Recipient.DoesNotExist:
                    not_found_countries.add(row.ISO3)
                except ValueError:
                    statistics["error_value"] += 1

            if len(not_found_countries) > 0:
                statistics["error_iso3"] = len(not_found_countries)
                print "Following countries not found:"
                for nfc in not_found_countries:
                    print nfc
            if statistics["error_value"] > 0:
                print "%d value errors" % statistics["error_value"]
