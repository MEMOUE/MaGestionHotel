from django.db import models
from django.conf import settings

class Chambre(models.Model):
    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='chambres'
    )
    numero_chambre = models.IntegerField(default=0)

    TYPE_SIMPLE = 'simple'
    TYPE_DOUBLE = 'double'
    TYPE_CHOICES = [
        (TYPE_SIMPLE, 'Simple'),
        (TYPE_DOUBLE, 'Double'),
    ]
    type_chambre = models.CharField(max_length=10, null=True, choices=TYPE_CHOICES)

    ETAT_LIBRE = 'libre'
    ETAT_OCCUPEE = 'occupee'
    ETAT_CHOICES = [
        (ETAT_LIBRE, 'Libre'),
        (ETAT_OCCUPEE, 'Occupée'),
    ]
    etat = models.CharField(max_length=10, null=False, choices=ETAT_CHOICES)

    STATUT_SALE = 'sale'
    STATUT_PROPRE = 'propre'
    STATUT_CHOICES = [
        (STATUT_SALE, 'Sale'),
        (STATUT_PROPRE, 'Propre'),
    ]
    statut = models.CharField(max_length=10, null=True, choices=STATUT_CHOICES)

    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.numero_chambre}"


class TypeChambre(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    typechambre = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.typechambre
