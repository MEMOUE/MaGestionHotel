from django.shortcuts import render
from reservation.models import Reservation, HistoriqueReservation
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from .forms import Statistiqueform
from datetime import date
from reservation.models import Reservation, HistoriqueReservation


def statistique(request):
    global date_de_reservation_historique, reservations_historiques, nombre_par_date, nombre_de_reservation
    if request.method == 'POST':
        form = Statistiqueform(request.POST)
        date_de_reservation_historique = []
        nombre_de_reservation = []
        nombre_par_date = 0

        if form.is_valid():
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']

            historiques = HistoriqueReservation.objects.filter(date_reservation__range=(date_debut, date_fin))
            reservations = Reservation.objects.filter(date_reservation__range=(date_debut, date_fin))
            reservations_historiques = list(reservations) + list(historiques)

            for data in reservations_historiques:
                if data.date_reservation not in date_de_reservation_historique:
                    date_de_reservation_historique.append(data.date_reservation)
    for dates in date_de_reservation_historique:
        for data in reservations_historiques:

            if dates == data.date_reservation:
                nombre_par_date += 1

        nombre_de_reservation.append(nombre_par_date)

    return render(request, "statistique/statistics.html")