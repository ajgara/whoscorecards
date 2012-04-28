from django.contrib import admin
import models

class CountryIndicatorAdmin(admin.ModelAdmin):
    list_filter = ("country", "indicator", "year")
    list_display = ("country", "indicator", "year", "value")

class AllocationAdmin(admin.ModelAdmin):
    list_filter = ("country", "mdgpurpose", "year")
    list_display = ("country", "mdgpurpose", "year", "commitment", "disbursement")

admin.site.register(models.Recipient)
admin.site.register(models.GeneralIndicator)
admin.site.register(models.CountryIndicator, CountryIndicatorAdmin)
admin.site.register(models.MDGPurpose)
admin.site.register(models.Allocation, AllocationAdmin)
