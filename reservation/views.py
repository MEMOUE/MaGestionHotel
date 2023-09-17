import io
from datetime import datetime
from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.pdfgen import canvas
from reservation.forms import ReservationForm
from reservation.models import Reservation
from .models import HistoriqueReservation
from chambre.models import Chambre


# Create your views here.


def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_reservation')
    else:
        form = ReservationForm()
    return render(request, 'reservation/reservation.html', {'form': form})


def liste_reservation(request):
    reservations = Reservation.objects.all()
    context = {'reservations': reservations}
    return render(request, 'reservation/liste_reservation.html', context)


def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('liste_reservation')
    else:
        form = ReservationForm(instance=reservation)

    return render(request, 'reservation/modifier_reservation.html', {'form': form})


def supprimer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        reservation.delete()
        return redirect('liste_reservation')

    return render(request, 'reservation/supprimer_reservation.html', {'reservation': reservation})


def genere_facture(request, id):
    temps = datetime.now()
    obj = Reservation.objects.get(id=id)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(300, 400))

    logo = "C:/Users/mamad/Documents/L3_GLSI/logotype.png"

    c.drawString(10, 380, "Nom : {}".format(obj.nom_client))
    c.drawString(10, 340, "Prenom : {}".format(obj.prenom_client))
    c.drawString(10, 300, "Adresse : {}".format(obj.adresse_client))
    c.drawString(10, 260, "Montant : {}".format(obj.nombre_jours))
    c.drawString(90, 260, "FCFA")
    c.drawString(10, 220, "Date réservation : {}".format(obj.date_reservation))
    c.drawString(10, 180, "Date arrivée : {}".format(obj.date_arrivee))
    c.drawImage(logo, 100, 50, width=100, height=100)
    c.drawString(75, 10, f"Fait le : "
                         f"{temps.day}-{temps.month}-{temps.year} à {temps.hour}h:{temps.minute}min:{temps.second}s"
                 )

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=obj.prenom_client + "_facture.pdf")


def copier_reservation_dans_historique(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)

        historique_reservation = HistoriqueReservation(

            nom_client=reservation.nom_client,
            prenom_client=reservation.prenom_client,
            adresse_client=reservation.adresse_client,
            date_reservation=reservation.date_reservation,
            date_arrivee=reservation.date_arrivee,
            nombre_jours=reservation.nombre_jours,
            chambre=reservation.chambre

        )

        historique_reservation.save()
        reservation.delete()

        return render(request, 'reservation/liste_reservation.html')  # Rediriger vers la liste des réservations
    except Reservation.DoesNotExist:
        return redirect('reservation/liste_reservation.html')  # Gérer le cas où la réservation n'existe pas


def liste_historique_reservations(request):
    historique_reservations = HistoriqueReservation.objects.all()

    context = {
        'historique_reservations': historique_reservations
    }

    return render(request, 'reservation/historique_reservations.html', context)


# Gestion de planning
def planning(request):
    planning_data = []
    chambres = Chambre.objects.all()
    reservations = Reservation.objects.all()
    historiques = HistoriqueReservation.objects.all()

    # Création d'une collection de dates uniques pour les réservations
    unique_dates = []
    for reservation in reservations:
        if reservation.date_reservation not in unique_dates:
            unique_dates.append(reservation.date_reservation)

    # Tri des dates uniques dans l'ordre croissant

    # Création d'une collection de dates uniques pour les historiques
    unique_dates_hist = []
    for historique in historiques:
        if historique.date_reservation not in unique_dates_hist:
            unique_dates.append(historique.date_reservation)

    # Tri des dates uniques
    unique_dates.sort()

    planning_data.append(
        {
            'chambres': chambres,
            'reservations': reservations,
            'unique_dates': unique_dates,
            'unique_dates_hist': unique_dates_hist,
            'historiques': historiques
        }
    )
    context = {
        'planning_data': planning_data
    }

    return render(request, 'reservation/planning.html', context)

#Representaion statistique des données

