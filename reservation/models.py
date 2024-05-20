from django.conf import settings
from django.db import models
from chambre.models import Chambre

class Reservation(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Modifié de OneToOneField à ForeignKey
    nom_client = models.CharField(max_length=50)
    prenom_client = models.CharField(max_length=150)
    date_arrivee = models.DateField(null=True)
    date_depart = models.DateField(null=True)
    adulte_suplementaire = models.IntegerField(null=True)
    enfant_suplementaire = models.IntegerField(null=True)
    paiement_anticipe = models.FloatField(max_length=100, default=0)
    frais_suplementaire = models.FloatField(max_length=100, default=0)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    STATUT_CHOICES = [
        ('reservée', 'Reservée'),
        ('confirmée', 'Confirmée'),
        ('terminée', 'Terminée'),
    ]
    statut = models.CharField(max_length=10, null=True, choices=STATUT_CHOICES)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_client} {self.prenom_client}"

class HistoriqueReservation(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Modifié de OneToOneField à ForeignKey
    nom_client = models.CharField(max_length=50)
    prenom_client = models.CharField(max_length=150)
    date_reservation = models.DateField(null=True)
    date_arrivee = models.DateField(null=True)
    paiement_anticipe = models.FloatField(max_length=100)
    adresse_client = models.FloatField(max_length=100, default=0)
    adulte_suplementaire = models.IntegerField(null=True)
    enfant_suplementaire = models.IntegerField(null=True)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    STATUT_CHOICES = [
        ('reservée', 'Reservée'),
        ('confirmée', 'Confirmée'),
        ('terminée', 'Terminée'),
    ]
    statut = models.CharField(max_length=10, null=True, choices=STATUT_CHOICES)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom_client} {self.prenom_client}"
