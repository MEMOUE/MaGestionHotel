from django.db import models
from django.urls import reverse
from HotelPlus import settings


# Create your models here.

class Configuration(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=200, blank=True)
    date_ajout = models.DateField(auto_now=True)

    def get_absolute_url(self):
        return reverse("confighotel:detail-config", kwargs={"pk": self.pk})

    def __str__(self):
        return self.nom


    

class PricingRule(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_heure_arrivee = models.DateTimeField()
    date_heure_depart = models.DateTimeField()
    tarif_supplementaire_adulte = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tarif_supplementaire_enfant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    frais_supplementaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Règle de prix {self.pk}"
