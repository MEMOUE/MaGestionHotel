from django.http import JsonResponse
from django.shortcuts import render
import plotly.graph_objs as go
from .forms import StatistiqueForm
from reservation.models import Reservation, HistoriqueReservation
from django.db.models import Count



from django.http import JsonResponse
from reservation.models import Reservation
import json

def statistics(request):
    reservations = Reservation.objects.all()

    reservations_data = []
    for reservation in reservations:
        reservation_data = {
            'date_arrivee': reservation.date_arrivee,
            'paiement_anticipe': reservation.paiement_anticipe,
            'frais_supplementaire': reservation.frais_supplementaire,
        }
        reservations_data.append(reservation_data)

    return render(request, 'statistique/statistics.html', {'reservations_data_json': json.dumps(reservations_data)})
