from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import re

import db
import oda.models as oda_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_largest_disbursements <data file>")

    
        re_name = re.compile("\s*\([^)]*\)\s*")
        filename = args[0]
        with transaction.commit_on_success():
            oda_models.Disbursement.objects.all().delete()
            dfactory = db.LargestDisbursementsFactory(file_path=filename, sheet_name="Sheet1")
            for row in dfactory.data:
                country = oda_models.Recipient.objects.get(iso3=row["ISO"])
                oda_models.Disbursement.objects.create(
                    country=country,
                    donor=re_name.sub("", row["Donor"]),
                    year=row["Year"],
                    purpose=row["Purpose"] or "",
                    disbursement=float(row["Disbursement"]),
                    percentage=float(row["%age"])
                )
