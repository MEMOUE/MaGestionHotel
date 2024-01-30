from django.urls import path
from .views import chambre_view, liste_chambre, modifier_chambre, supprimer_chambre

urlpatterns = [
    path('add/', chambre_view, name='chambre'),
    path('', liste_chambre, name='liste_chambre'),
    path('chambre/modifier/<int:chambre_id>/', modifier_chambre, name='modifier_chambre'),
    path('chambre/supprimer/<int:chambre_id>/', supprimer_chambre, name='supprimer_chambre'),
]