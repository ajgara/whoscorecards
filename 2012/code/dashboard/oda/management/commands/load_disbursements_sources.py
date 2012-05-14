from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import db
import oda.models as oda_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_disbursements_sources <data file>")

    
        filename = args[0]
        with transaction.commit_on_success():
            oda_models.DisbursementSource.objects.all().delete()
            source_factory = db.ODASourceFactory(file_path=filename, sheet_name="DB")
            for row in source_factory.data:
                country = oda_models.Recipient.objects.get(iso3=row["ISO"])
                oda_models.DisbursementSource.objects.create(
                    country=country,
                    source=row["donorname"],
                    number=int(row["Number of disbursement"]),
                    amount=float(row["Amount disbursed M constant 2009 USD"]),
                    group=row["Group"]
                )
