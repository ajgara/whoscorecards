from django.contrib import admin
import models

class CountryIndicatorAdmin(admin.ModelAdmin):
    list_filter = ("country", "indicator", "year")
    list_display = ("country", "indicator", "year", "value")

admin.site.register(models.Recipient)
admin.site.register(models.GeneralIndicator)
admin.site.register(models.CountryIndicator, CountryIndicatorAdmin)
