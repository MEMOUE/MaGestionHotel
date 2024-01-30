from django.http import JsonResponse
from django.shortcuts import render
import plotly.graph_objs as go
from .forms import StatistiqueForm
from reservation.models import Reservation, HistoriqueReservation
from django.db.models import Count


def statistics(request):
    # Filtrer les réservations pour l'utilisateur connecté
    user_reservations = Reservation.objects.filter(proprietaire=request.user)

    # Nombre total de réservations pour l'utilisateur connecté
    total_reservations = user_reservations.count()

    # Nombre de réservations par statut pour l'utilisateur connecté
    reservations_by_status = user_reservations.values('statut').annotate(count=Count('id'))

    context = {
        'total_reservations': total_reservations,
        'reservations_by_status': reservations_by_status,
        # Ajoutez d'autres variables contextuelles au besoin
    }
    return render(request, "statistique/statistics.html",context)
