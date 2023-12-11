from django.shortcuts import render
import plotly.graph_objs as go
from .forms import StatistiqueForm
from reservation.models import Reservation, HistoriqueReservation


def statistics(request):
    date_de_reservation_historique = []
    nombre_de_reservation = []
    reservations_historiques = []
    nombre_par_date = 0

    if request.method == 'POST':
        form = StatistiqueForm(request.POST)

        if form.is_valid():
            date_debut = form.cleaned_data['date_debut']
            date_fin = form.cleaned_data['date_fin']

            historiques = HistoriqueReservation.objects.filter(date_reservation__range=(date_debut, date_fin))
            reservations = Reservation.objects.filter(date_reservation__range=(date_debut, date_fin))
            reservations_historiques = list(reservations) + list(historiques)

            for data in reservations_historiques:
                if data.date_reservation not in date_de_reservation_historique:
                    date_de_reservation_historique.append(data.date_reservation)
        # Pas de redirection, réafficher simplement le formulaire avec des erreurs
        else:
            context = {'form': form}
            return render(request, "statistique/statistics.html", context)
    else:
        form = StatistiqueForm()

    for dates in date_de_reservation_historique:
        for data in reservations_historiques:
            if dates == data.date_reservation:
                nombre_par_date += 1

        nombre_de_reservation.append(nombre_par_date)

    # Création du graphique à barres
    x_data = date_de_reservation_historique
    y_data = nombre_de_reservation

    bar_trace = go.Bar(
        
        x=x_data,
        y=y_data,
        marker=dict(color='blue'),
    )

    layout = go.Layout(
        title='Exemple de graphique à barres avec Plotly',
        xaxis=dict(title='Date de réservation'),
        yaxis=dict(title='Nombre de réservation'),
    )

    fig = go.Figure(data=[bar_trace], layout=layout)

    # Convertir la figure en JSON
    graph_json = fig.to_json()

    # Transmettre les données du graphique et le formulaire au modèle
    context = {
        'form': form,  # Ajouter le formulaire au contexte
        'graph': graph_json,  # Transmettre le graphique JSON au modèle
    }

    return render(request, "statistique/statistics.html", context)
