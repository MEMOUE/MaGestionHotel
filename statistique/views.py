import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
import plotly.graph_objs as go
from .forms import StatistiqueForm
from reservation.models import Reservation, HistoriqueReservation
from django.db.models import Count

def statistics(request):
    reservations = Reservation.objects.filter(proprietaire=request.user)

    # Convertir les objets de date en chaînes de caractères
    reservations_data = [
        {
            'date_arrivee': reservation.date_arrivee.strftime('%Y-%m-%d'),
            'paiement_anticipe': reservation.paiement_anticipe,
            'frais_supplementaire': reservation.frais_suplementaire,
        }
        for reservation in reservations
    ]

    return render(request, 'statistique/statistics.html', {'reservations_data_json': json.dumps(reservations_data)})
