from django.urls import path
from .views import chambre_view, liste_chambre, modifier_chambre, supprimer_chambre,typechambre_list,typechambre_new,typechambre_edit,typechambre_delete

urlpatterns = [
    path('add/', chambre_view, name='chambre'),
    path('', liste_chambre, name='liste_chambre'),
    path('chambre/modifier/<int:chambre_id>/', modifier_chambre, name='modifier_chambre'),
    path('chambre/supprimer/<int:chambre_id>/', supprimer_chambre, name='supprimer_chambre'),

    path('typechambre_list', typechambre_list, name='typechambre_list'),
    path('typechambre/new/', typechambre_new, name='typechambre_new'),
    path('typechambre/<int:pk>/edit/', typechambre_edit, name='typechambre_edit'),
    path('typechambre/<int:pk>/delete/', typechambre_delete, name='typechambre_delete'),

]