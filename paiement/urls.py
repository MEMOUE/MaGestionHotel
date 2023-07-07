from django.urls import path

from paiement.views import home_paiement

urlpatterns = [
    path("", home_paiement, name="home_paiement"),
]