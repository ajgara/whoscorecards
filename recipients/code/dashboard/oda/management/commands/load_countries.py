import csv

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import oda.models as oda_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Usage load_counties <countries file>")

        reader = csv.reader(open(args[0]))
        with transaction.commit_on_success():
            for row in reader:
                oda_models.Recipient.objects.get_or_create(
                    iso3=row[0], 
                    name=row[1]
                )
