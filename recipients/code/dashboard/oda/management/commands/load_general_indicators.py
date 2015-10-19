from django.core.management.base import BaseCommand, CommandError
from django.utils import translation
import db
import oda.models as oda_models
from collections import defaultdict
import sys
from django.db import transaction

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_general_indicators <indicator file>")

    
        with transaction.commit_on_success():
            statistics = defaultdict(int, {})
            fn_indicator = args[0]
            indicators_factory = db.IndicatorsFactory(file_path=fn_indicator, sheet_name="Table1")

            countries = {}
            not_found_countries = set()
            indicators = {}
            total = len(indicators_factory.data)
            count = 0
            for row in indicators_factory.data:
                count += 1
                year = str(int(row.Year))
                #sys.stdout.write("\r%d of %d" % (count, total))
                #sys.stdout.flush()
                try:
                    if row.ISO3 in countries:
                        country = countries[row.ISO3]
                    else:
                        country, _ = oda_models.Recipient.objects.get_or_create(
                            iso3=row.ISO3
                        )
                        country.name = row["WHO Name"]
                        country.save()
                        countries[row.ISO3] = country

                    if row.Indicators in indicators:
                        indicator = indicators[row.Indicators]
                    else:
                        indicator, _ = oda_models.GeneralIndicator.objects.get_or_create(name=row.Indicators)
                        indicators[row.Indicators] = indicator

                    oda_models.CountryIndicator.objects.filter(
                        country=country, 
                        indicator=indicator,
                        year=year,
                    ).delete()
                    ci_ = oda_models.CountryIndicator.objects.create(
                        country=country, 
                        indicator=indicator, 
                        year=year,
                        raw_value=row.Value
                    )
                    ci_.value = float(row.Value)
                    ci_.save()
                except oda_models.Recipient.DoesNotExist:
                    not_found_countries.add(row.ISO3)
                except ValueError:
                    import traceback
                    traceback.print_exc()
                    print "Error when casting value '%s' for '%s'." % (row.Value, row.ISO3)
                    statistics["error_value"] += 1

            if len(not_found_countries) > 0:
                statistics["error_iso3"] = len(not_found_countries)
                print "Following countries not found:"
                for nfc in not_found_countries:
                    print nfc
            if statistics["error_value"] > 0:
                print "%d value errors" % statistics["error_value"]
