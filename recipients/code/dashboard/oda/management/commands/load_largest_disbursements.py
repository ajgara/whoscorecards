from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import re

import db
import oda.models as oda_models

class Command(BaseCommand):
    DONOR_NAME_OVERRIDES = {
        'Bill & Melinda Gates Foundation': 'BMGF',
        'The Global Fund to Fight AIDS, Tuberculosis and Malaria': 'The Global Fund'
    }

    def get_donor_name(self, donor):
        donor = donor.strip()
        if donor in self.DONOR_NAME_OVERRIDES:
            return self.DONOR_NAME_OVERRIDES[donor]
        return donor

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_largest_disbursements <data file>")

        # re_name = re.compile("\s*\([^)]*\)\s*")
        filename = args[0]
        with transaction.commit_on_success():
            oda_models.Disbursement.objects.all().delete()
            dfactory = db.LargestDisbursementsFactory(file_path=filename, sheet_name="DB")
            for row in dfactory.data:
                country = oda_models.Recipient.objects.get(iso3=row["ISO"])
                oda_models.Disbursement.objects.create(
                    country=country,
                    donor=self.get_donor_name(row["Donor"]),
                    year=row["Year"],
                    purpose=row["Purpose"] or "",
                    percentage=float(row["%age"]),
                    disbursement=float(row["Total Disbursements"] or 0)
                )
