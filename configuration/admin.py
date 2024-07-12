from django.contrib import admin

from configuration.models import Configuration,  PricingRule

# Register your models here.


class AdminConfiguration(admin.ModelAdmin):
    list_display = ("nom", "adresse", "telephone", "date_ajout")

    class Media:
        js = ("js/admin.js", )
        css = {
            "all": ("css/admin.css", )
        }



admin.site.register(Configuration, AdminConfiguration)
admin.site.register(PricingRule)