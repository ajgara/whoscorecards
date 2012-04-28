from django.db import models

class Country(models.Model):

    name = models.CharField(max_length=60)
    iso3 = models.CharField(max_length=3)

    class Meta:
        abstract = True

class Recipient(Country):
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.iso3)

class GeneralIndicator(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

class CountryIndicator(models.Model):
    country = models.ForeignKey(Recipient)
    indicator = models.ForeignKey(GeneralIndicator)
    year = models.CharField(max_length=4)
    value = models.FloatField()

    class Meta:
        unique_together = ("country", "indicator", "year")

    def __unicode__(self):
        return "%s (%s)" % (self.indicator, self.country.iso3)

class MDGPurpose(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "MDG Purposes" 

class Allocation(models.Model):
    country = models.ForeignKey(Recipient)
    mdgpurpose = models.ForeignKey(MDGPurpose)
    year = models.CharField(max_length=4)
    commitment = models.FloatField()
    disbursement = models.FloatField()

    def __unicode__(self):
        return "%s - %s (%s)" % (self.country, self.mdgpurpose, self.year)
