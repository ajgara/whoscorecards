from django.db import models

class Country(models.Model):

    name = models.CharField(max_length=60)
    iso3 = models.CharField(max_length=3, unique=True)

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
    value = models.FloatField(null=True)

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
    commitment = models.FloatField(null=True)
    disbursement = models.FloatField(null=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.country, self.mdgpurpose, self.year)

class DisbursementSource(models.Model):
    country = models.ForeignKey(Recipient)
    source = models.CharField(max_length=50)
    number = models.IntegerField()
    amount = models.FloatField()
    group = models.CharField(max_length=10, choices=(("Bil", "Bil"), ("Mul", "Mul"), ("Phil", "Phil")))

    def __unicode__(self):
        return "%s => %s" % (self.source, self.country)
    
class Disbursement(models.Model):
    country = models.ForeignKey(Recipient)
    donor = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    purpose = models.CharField(max_length=50)
    disbursement = models.FloatField()
    percentage = models.FloatField()

    def __unicode__(self):
        return "%s (%s)" % (self.donor, self.purpose)

class Largest5Disbursements(models.Model):
    country = models.ForeignKey(Recipient)
    donor = models.CharField(max_length=50)
    disbursement = models.FloatField()
    percentage = models.FloatField()

    def __unicode__(self):
        return "%s (%s)" % (self.donor, self.purpose)
