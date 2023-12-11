from django.urls import path
from . import views

from reservation.views import reservation_view, modifier_reservation, supprimer_reservation, liste_reservation, \
    genere_facture,liste_historique_reservations,planning

urlpatterns = [
    
    path('', liste_reservation, name='liste_reservation'),
    path('add/', reservation_view, name='add_reservation'),
    path('modifier_reservation/<int:reservation_id>/', modifier_reservation, name='modifier_reservation'),
    path('supprimer_reservation/<int:reservation_id>/', supprimer_reservation, name='supprimer_reservation'),
    path("facture/<int:id>", genere_facture, name="facture_pdf"),
    
    path('copier_reservation_dans_historique/<int:reservation_id>/', views.copier_reservation_dans_historique, name='copier_reservation_dans_historique'),
    path('historique_reservations/', liste_historique_reservations, name='historique_reservations'),

    path('planning/',planning, name='planning'),
]