from django.db import models

# Create your models here.


class Reservation(models.Model):
    nom_client = models.CharField(max_length=50)
    prenom_client = models.CharField(max_length=150)
    adresse_client = models.CharField(max_length=100)
    date_reservation = models.DateField(auto_now=True)
    date_arrivee = models.DateField(null=True)
    nombre_jours = models.IntegerField(null=True)
    chambre = models.CharField(max_length=10)