from django.db import models

class Country(models.Model):

    name = models.CharField(max_length=60)
    iso3 = models.CharField(max_length=3)

    class Meta:
        abstract = True

class Recipient(Country):
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.iso3)
