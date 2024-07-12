from django.conf import settings
from django.db import models
from chambre.models import Chambre

class UserInvoiceCounter(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_invoice_number = models.IntegerField(default=0)

class BaseReservation(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nom_client = models.CharField(max_length=50)
    prenom_client = models.CharField(max_length=150)
    date_arrivee = models.DateField(null=True)
    date_depart = models.DateField(null=True)
    adulte_suplementaire = models.IntegerField(null=True)
    enfant_suplementaire = models.IntegerField(null=True)
    paiement_anticipe = models.FloatField(default=0)
    frais_suplementaire = models.FloatField(default=0)
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    STATUT_CHOICES = [
        ('reservée', 'Reservée'),
        ('confirmée', 'Confirmée'),
        ('terminée', 'Terminée'),
    ]
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, null=True)
    note = models.TextField(blank=True, null=True)
    numero_facture = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nom_client} {self.prenom_client}"

class Reservation(BaseReservation):
    pass

class HistoriqueReservation(BaseReservation):
    class Meta:
        verbose_name = "Historique de Réservation"
        verbose_name_plural = "Historiques de Réservation"
