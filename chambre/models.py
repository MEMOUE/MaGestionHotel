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

    type_chambre = models.ForeignKey(
        'TypeChambre',
        on_delete=models.SET_NULL,
        null=True,
        related_name='chambres'
    )

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
