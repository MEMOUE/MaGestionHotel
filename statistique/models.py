from django.db import models


class Statistique(models.Model):
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)

    def __str__(self):
        return f"{self.date_debut} - {self.date_fin}"
