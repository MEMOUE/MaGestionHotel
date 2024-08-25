from django.utils import timezone
from django.db import models

from HotelPlus import settings
from reservation.models import Reservation


# Create your models here.
class Restaurant(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom_menu = models.CharField(max_length=150)
    image = models.ImageField(upload_to="resto", blank=True, null=True)
    prix_origine = models.FloatField(default=0.0)
    prix_vente = models.FloatField(default=0.0)

    def __str__(self):
        return self.nom_menu
    

class Commande(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    plat = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_commande = models.DateTimeField(default=timezone.now)
    quantite = models.PositiveIntegerField(default=1)
    prix_total = models.FloatField(default=0.0)
    annulee = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.prix_total = self.quantite * self.plat.prix_vente
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} - {self.reservation.nom_client} {self.reservation.prenom_client}"
