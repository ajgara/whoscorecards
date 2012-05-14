from django.contrib import admin
import models

class CountryIndicatorAdmin(admin.ModelAdmin):
    list_filter = ("country", "indicator", "year")
    list_display = ("country", "indicator", "year", "value")

class AllocationAdmin(admin.ModelAdmin):
    list_filter = ("country", "mdgpurpose", "year")
    list_display = ("country", "mdgpurpose", "year", "commitment", "disbursement")

class DisbursementSourceAdmin(admin.ModelAdmin):
    list_filter = ("country", "source", "group")
    list_display = ("country", "source", "number", "amount", "group")

class DisbursementAdmin(admin.ModelAdmin):
    list_filter = ("country", "donor", "year", "purpose")
    list_display = ("country", "donor", "year", "purpose", "disbursement", "percentage")

admin.site.register(models.Recipient)
admin.site.register(models.GeneralIndicator)
admin.site.register(models.CountryIndicator, CountryIndicatorAdmin)
admin.site.register(models.MDGPurpose)
admin.site.register(models.Allocation, AllocationAdmin)
admin.site.register(models.DisbursementSource, DisbursementSourceAdmin)
admin.site.register(models.Disbursement, DisbursementAdmin)
