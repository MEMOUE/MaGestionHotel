from django.contrib.auth.models import AbstractUser, Group, Permission,  BaseUserManager
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string


class Users(AbstractUser):
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.email_verification_token:
            self.email_verification_token = get_random_string(length=64)
        super().save(*args, **kwargs)



from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class SecondaryUser(models.Model):
    username = models.CharField(_('username'), max_length=150, unique=True)
    hashed_password = models.CharField(_('hashed password'), max_length=128, blank=True)
    nom = models.CharField(_('nom'), max_length=100)
    prenom = models.CharField(_('prénom'), max_length=100)
    
    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='secondary_users'
    )
    
    can_access_chambres = models.BooleanField(default=False)
    can_access_resto = models.BooleanField(default=False)
    can_access_configuration = models.BooleanField(default=False)
    can_access_reservation = models.BooleanField(default=False)
    can_access_paiements = models.BooleanField(default=False)
    can_access_statistics = models.BooleanField(default=False)
    can_access_history = models.BooleanField(default=False)
    can_access_settings = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Utilisateur secondaire"
        verbose_name_plural = "Utilisateurs secondaires"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

    def save(self, *args, **kwargs):
        if self.pk is None:  # Nouvel utilisateur
            self.hashed_password = make_password(self.hashed_password)
        super().save(*args, **kwargs)
