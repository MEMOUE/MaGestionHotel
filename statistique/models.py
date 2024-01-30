from django.db import models

from HotelPlus import settings


class Statistique(models.Model):


    def __str__(self):
        return f"{self.date_debut} - {self.date_fin}"
