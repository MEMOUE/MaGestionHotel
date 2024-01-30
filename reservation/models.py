from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from chambre.models import Chambre


# Create your models here.
class Reservation(models.Model):
    proprietaire = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom_client = models.CharField(max_length=50)
    prenom_client = models.CharField(max_length=150)
    adresse_client = models.CharField(max_length=100)
    date_reservation = models.DateField(null=True)
    date_arrivee = models.DateField(null=True)
    nombre_jours = models.IntegerField(null=True)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    STATUT_CHOICES = [
        ('reservée', 'Reservée'),
        ('confirmée', 'Confirmée'),
        ('terminée', 'Terminée'),
    ]
    statut = models.CharField(max_length=10, null=True, choices=STATUT_CHOICES)

    def __str__(self):
        return f"{self.nom_client}{self.prenom_client}"


class HistoriqueReservation(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    nom_client = models.CharField(max_length=50)
    prenom_client = models.CharField(max_length=150)
    adresse_client = models.CharField(max_length=100)
    date_reservation = models.DateField(auto_now=True)
    date_arrivee = models.DateField(null=True)
    nombre_jours = models.IntegerField(null=True)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    STATUT_CHOICES = [
        ('reservée', 'Reservée'),
        ('confirmée', 'Confirmée'),
        ('terminée', 'Terminée'),
    ]
    statut = models.CharField(max_length=10, null=True, choices=STATUT_CHOICES)

    def __str__(self):
        return f"{self.nom_client}{self.prenom_client}"
