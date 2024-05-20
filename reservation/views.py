import io
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.pdfgen import canvas
from reservation.forms import ReservationForm
from reservation.models import Reservation
from .models import HistoriqueReservation
from chambre.models import Chambre


# Create your views here.


@login_required
def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.user, request.POST)  # Passer request.user comme argument
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.proprietaire = request.user
            reservation.save()
            return redirect('planning')
    else:
        form = ReservationForm(user=request.user)  # Passer request.user comme argument

    return render(request, 'reservation/reservation.html', {'form': form})


from datetime import datetime

@login_required
def liste_reservation(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        # Convertir les dates saisies en objets datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filtrer les réservations en fonction de l'intervalle de dates
        reservations = Reservation.objects.filter(proprietaire=request.user, date_arrivee__gte=start_date, date_arrivee__lte=end_date)
    else:
        # Si aucune date n'est saisie, afficher toutes les réservations de l'utilisateur
        reservations = Reservation.objects.filter(proprietaire=request.user)

    context = {'reservations': reservations}
    return render(request, 'reservation/liste_reservation.html', context)


@login_required
def modifier_reservation(request, reservation_id):
    # Récupérer la réservation à modifier
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Assurez-vous que seul le propriétaire peut modifier la réservation
    if request.user != reservation.proprietaire:
        return HttpResponseForbidden("Vous n'avez pas la permission de modifier cette réservation.")

    if request.method == 'POST':
        form = ReservationForm(request.user, request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('planning')
    else:
        form = ReservationForm(user=request.user, instance=reservation)

    return render(request, 'reservation/modifier_reservation.html', {'form': form, 'reservation': reservation})


def supprimer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        reservation.delete()
        return redirect('planning')

    return render(request, 'reservation/supprimer_reservation.html', {'reservation': reservation})


def genere_facture(request, id):
    temps = datetime.now()
    obj = Reservation.objects.get(id=id)
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(300, 400))

    #logo = "C:/Users/mamad/Documents/L3_GLSI/logotype.png"

    c.drawString(10, 380, "Nom : {}".format(obj.nom_client))
    c.drawString(10, 340, "Prenom : {}".format(obj.prenom_client))
    c.drawString(10, 300, "Adresse : {}".format(obj.adresse_client))
    c.drawString(10, 260, "Montant : {}".format(obj.nombre_jours))
    c.drawString(90, 260, "FCFA")
    c.drawString(10, 220, "Date réservation : {}".format(obj.date_reservation))
    c.drawString(10, 180, "Date arrivée : {}".format(obj.date_arrivee))
    #c.drawImage(logo, 100, 50, width=100, height=100)
    c.drawString(75, 10, f"Fait le : "
                         f"{temps.day}-{temps.month}-{temps.year} à {temps.hour}h:{temps.minute}min:{temps.second}s"
                 )

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=obj.prenom_client + "_facture.pdf")


@login_required
def copier_reservation_dans_historique(request, reservation_id):
    # Récupérer la réservation à partir de l'ID
    reservation = get_object_or_404(Reservation, id=reservation_id, proprietaire=request.user)

    # Créer une nouvelle instance d'HistoriqueReservation avec les données de la réservation
    HistoriqueReservation.objects.create(
        proprietaire=reservation.proprietaire,
        nom_client=reservation.nom_client,
        prenom_client=reservation.prenom_client,
        date_reservation=reservation.date_arrivee,  # Assurez-vous d'utiliser la bonne date si vous avez une autre date de réservation
        date_arrivee=reservation.date_arrivee,
        paiement_anticipe=reservation.paiement_anticipe,
        adulte_suplementaire=reservation.adulte_suplementaire,
        enfant_suplementaire=reservation.enfant_suplementaire,
        chambre=reservation.chambre,
        statut=reservation.statut,
        note=reservation.note
        # adresse_client est exclu car il n'existe pas dans le modèle Reservation
    )

    # Supprimer la réservation originale
    reservation.delete()

    # Rediriger vers la page de planning
    return redirect('planning')

def liste_historique_reservations(request):
    historique_reservations = HistoriqueReservation.objects.filter(proprietaire=request.user)

    context = {
        'historique_reservations': historique_reservations
    }

    return render(request, 'reservation/historique_reservations.html', context)


def planning(request):
    chambres = Chambre.objects.filter(proprietaire=request.user)
    reservations = Reservation.objects.filter(proprietaire=request.user)
    historiques = HistoriqueReservation.objects.filter(proprietaire=request.user)

    dates_reservations = set(reservation.date_arrivee for reservation in reservations)
    dates_historiques = set(historique.date_arrivee for historique in historiques)
    dates_uniques = sorted(dates_reservations.union(dates_historiques))

    planning_data = []
    for chambre in chambres:
        chambre_data = {
            'numero_chambre': chambre.numero_chambre,
            'prix': chambre.prix,
            'reservations': [],
        }
        for date in dates_uniques:
            reservation = reservations.filter(chambre=chambre, date_arrivee=date).first()

            if reservation:
                chambre_data['reservations'].append({
                    'date': date,
                    'id': reservation.id,
                    'nom_client': reservation.nom_client,
                    'prenom_client': reservation.prenom_client,
                    'statut': reservation.statut,
                    'date_arrivee': reservation.date_arrivee,
                    'date_depart': reservation.date_depart,
                    'nombre_jours': (reservation.date_depart - reservation.date_arrivee).days if reservation.date_depart and reservation.date_arrivee else '',
                    'chambre': reservation.chambre.numero_chambre,
                    'note': reservation.note,
                })
            else:
                chambre_data['reservations'].append({
                    'date': date,
                    'nom_client': '',
                    'prenom_client': '',
                    'statut': 'vide',
                })

        planning_data.append(chambre_data)

    context = {'planning_data': planning_data, 'dates_uniques': dates_uniques}
    return render(request, 'reservation/planning.html', context)