import json
import os
from django.core.management.base import BaseCommand, CommandError
import requests
import oda.models as oda_models
from StringIO import StringIO

class Command(BaseCommand):
    def handle(self, *args, **options):
    
        url = "http://192.168.56.101:5000/ajax/convert/"
        fileurl = "http://192.168.56.101/static"
        outfolder = "/tmp/who"
        for recipient in oda_models.Recipient.objects.all():
            params = {
                "url" : "http://192.168.56.1:8000/oda/scorecard/%s/" % recipient.iso3,
                "ext" : ".pdf",
                "pages" : 2
            }

            print recipient.iso3
            r = requests.get(url, params=params)
            js = json.loads(r.text)
            if js["status"] == "OK":
                fn = js["data"]
                output_url = "%s/%s/%s" % (fileurl, fn[0:2], fn)
                r2 = requests.get(output_url)
                
                fname = "%s - %s.pdf" % (recipient.name, recipient.iso3)
                fp = open(os.path.join(outfolder, fname), "wb")
                fp.write(r2.content)
                fp.close()
            else:
                print "Error generating pdf"
