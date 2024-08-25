from django.urls import path
from . import views

from reservation.views import reservation_view, modifier_reservation, supprimer_reservation, liste_reservation, \
    genere_et_affiche_facture,liste_historique_reservations,planning, details_reservation

urlpatterns = [

    path('', liste_reservation, name='liste_reservation'),
    path('add/', reservation_view, name='add_reservation'),
    path('modifier_reservation/<int:reservation_id>/', modifier_reservation, name='modifier_reservation'),
    path('supprimer_reservation/<int:reservation_id>/', supprimer_reservation, name='supprimer_reservation'),
    path('copier_reservation_dans_historique/<int:reservation_id>/', views.copier_reservation_dans_historique, name='copier_reservation_dans_historique'),
    path('historique_reservations/', liste_historique_reservations, name='historique_reservations'),

    #urls de la fenetre du tableau de bord

    path('planning/copier_reservation_dans_historique/<int:reservation_id>/', views.copier_reservation_dans_historique, name='reservation_dans_historique'),
    path('planning/', planning, name='planning'),
    path('planning/modifier_reservation/<int:reservation_id>/', modifier_reservation, name='modifie'),
    path('planning/supprimer_reservation/<int:reservation_id>/', supprimer_reservation, name='supprimer'),
    path('planning/details_reservation/<int:reservation_id>/', details_reservation, name='details_reservation'),
    path('planning/genere_et_affiche_facture/<int:reservation_id>/', genere_et_affiche_facture,name='genere_et_affiche_facture'),
]