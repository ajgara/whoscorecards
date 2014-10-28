from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import db
import oda.models as oda_models

class Command(BaseCommand):
    SOURCE_NAME_OVERRIDES = {
        'Bill & Melinda Gates Foundation': 'BMGF',
        'The Global Fund to Fight AIDS, Tuberculosis and Malaria': 'The Global Fund'
    }

    def get_source_name(self, donor):
        donor = donor.strip()
        if donor in self.SOURCE_NAME_OVERRIDES:
            return self.SOURCE_NAME_OVERRIDES[donor]
        return donor

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_disbursements_sources <data file>")
    
        filename = args[0]
        with transaction.commit_on_success():
            oda_models.DisbursementSource.objects.all().delete()
            source_factory = db.ODASourceFactory(file_path=filename, sheet_name="DB")
            for row in source_factory.data:
                print row["ISO"]
                country = oda_models.Recipient.objects.get(iso3=row["ISO"])

                oda_models.DisbursementSource.objects.create(
                    country=country,
                    source=self.get_source_name(row["donorname"]),
                    number=int(row["Number of disbursements"]),
                    amount=float(row["Amount disbursed"]),
                    group=row["Group"]
                )
