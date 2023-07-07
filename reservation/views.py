import io
from datetime import datetime

from django.http import FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from reportlab.pdfgen import canvas

from reservation.forms import ReservationForm
from reservation.models import Reservation


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
    return FileResponse(buffer, as_attachment=True, filename=obj.prenom_client+"_facture.pdf")