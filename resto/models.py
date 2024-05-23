from django.db import models

from HotelPlus import settings


# Create your models here.
class Restaurant(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom_menu = models.CharField(max_length=150)
    image = models.ImageField(upload_to="resto", blank=True, null=True)
    prix_origine = models.FloatField(default=0.0)
    prix_vente = models.FloatField(default=0.0)
