from django.contrib import admin
from resto.models import Restaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("nom_menu", "prix_origine", "prix_vente")
    search_fields = ["nom_menu", "prix_origine", "prix_vente"]

    class Media:
        js = ("js/admin.js", )
        css = {
            "all": ("css/admin.css", )
        }
