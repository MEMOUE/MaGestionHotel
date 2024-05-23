from django.db import models
from django.db import models
from django.conf import settings

class AutreRevenuCout(models.Model):
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    temps = models.DateTimeField()
    type = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()

    def __str__(self):
        return f"{self.type} - {self.temps}"
