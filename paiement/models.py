from django.db import models
from django.db import models
from django.conf import settings

class AutreRevenuCout(models.Model):
    REVENUE_TYPE_CHOICES = [
        ('coût', 'Coût'),
        ('revenu', 'Revenu'),
    ]
    
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    type = models.CharField(
        max_length=100, 
        choices=REVENUE_TYPE_CHOICES, 
        blank=True, 
        null=True,
        help_text="Choisissez entre Coût ou Revenu"
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()

    def __str__(self):
        return f"{self.get_type_display()} - {self.montant}"

    

from django.db import models
from django.conf import settings
from datetime import timedelta

class Subscription(models.Model):
    DURATION_CHOICES = [
        (3, '3 mois'),
        (6, '6 mois'),
        (9, '9 mois'),
        (12, '12 mois'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(choices=DURATION_CHOICES)
    is_active = models.BooleanField(default=False)

    def end_date(self):
        return self.start_date + timedelta(days=30*self.duration)

    def __str__(self):
        return f"{self.user.username} - {self.get_duration_display()}"

    def activate(self):
        self.is_active = True
        self.save()
