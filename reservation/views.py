import io
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.pdfgen import canvas
from reservation.forms import ReservationForm
from reservation.models import Reservation, HistoriqueReservation, UserInvoiceCounter
from chambre.models import Chambre
from decimal import Decimal
from configuration.models import Configuration
from django.db import transaction
from datetime import datetime
from decimal import Decimal
import io
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.shortcuts import get_object_or_404

    # Assuming Configuration is correctly imported from the correct module
from configuration.models import Configuration
from .models import Reservation



@login_required
def reservation_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.user, request.POST)
        if form.is_valid():
            with transaction.atomic():
                reservation = form.save(commit=False)
                reservation.proprietaire = request.user

                # Générer un numéro de facture unique et croissant pour chaque utilisateur
                invoice_counter, created = UserInvoiceCounter.objects.get_or_create(user=request.user)
                invoice_counter.last_invoice_number += 1
                reservation.numero_facture = f"{invoice_counter.last_invoice_number}"
                invoice_counter.save()

                reservation.save()
            return redirect('planning')
    else:
        form = ReservationForm(user=request.user)

    return render(request, 'reservation/reservation.html', {'form': form})

@login_required
def liste_reservation(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        reservations = Reservation.objects.filter(proprietaire=request.user, date_arrivee__gte=start_date, date_arrivee__lte=end_date)
    else:
        reservations = Reservation.objects.filter(proprietaire=request.user)

    context = {'reservations': reservations}
    return render(request, 'reservation/liste_reservation.html', context)

@login_required
def modifier_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
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

@login_required
def genere_facture(request, id):
    # Récupérer l'objet Reservation
    obj = get_object_or_404(Reservation, id=id, proprietaire=request.user)
    
    # Récupérer la configuration de l'utilisateur connecté
    configuration = get_object_or_404(Configuration, proprietaire=request.user)
    
    # Buffer pour la génération du PDF
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(300, 400))
    
    # Calculer le nombre de jours
    nombre_jours = (obj.date_depart - obj.date_arrivee).days if obj.date_depart and obj.date_arrivee else 0
    
    # Calculer le montant total
    chambre_prix = Decimal(obj.chambre.prix)
    paiement_anticipe = Decimal(obj.paiement_anticipe)
    frais_suplementaire = Decimal(obj.frais_suplementaire)
    montant_total = nombre_jours * chambre_prix + frais_suplementaire - paiement_anticipe
    
    # Dessiner les informations de l'entreprise
    if configuration:
        c.setFont("Helvetica", 16)
        c.drawString(10, 380, configuration.nom)
        c.setFont("Helvetica", 12)
        c.drawString(10, 360, "Téléphone : {}".format(configuration.telephone))
        c.drawString(10, 340, "Adresse : {}".format(configuration.adresse))
    
    # Extraire seulement la partie souhaitée du numéro de facture
    facture_numero = obj.numero_facture.split('-')[0] if '-' in obj.numero_facture else obj.numero_facture
    
    # Dessiner les détails de la réservation
    c.setFont("Helvetica-Bold", 16)
    c.drawString(10, 320, "Facture N° {}".format(facture_numero))
    c.line(10, 315, 150, 315)
    
    c.setFont("Helvetica", 12)
    c.drawString(10, 300, "Nom : {}".format(obj.nom_client))
    c.drawString(10, 280, "Prénom : {}".format(obj.prenom_client))
    c.drawString(10, 260, "Date arrivée : {}".format(obj.date_arrivee.strftime('%d-%m-%Y')))
    c.drawString(10, 240, "Date départ : {}".format(obj.date_depart.strftime('%d-%m-%Y')))
    c.drawString(10, 220, "Chambre : {}".format(obj.chambre.numero_chambre))
    c.drawString(10, 200, "Adultes supplémentaires : {}".format(obj.adulte_suplementaire))
    c.drawString(10, 180, "Enfants supplémentaires : {}".format(obj.enfant_suplementaire))
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(10, 160, "Montant total à payer : {} FCFA".format(montant_total))
    c.line(10, 155, 220, 155)
    
    c.setFont("Helvetica", 10)
    temps = datetime.now()
    c.drawString(10, 10, "Fait le : {}-{}-{} à {}h:{}min:{}s".format(
        temps.day, temps.month, temps.year, temps.hour, temps.minute, temps.second
    ))
    
    # Finaliser le PDF
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="facture_{}_{}.pdf".format(facture_numero, obj.nom_client))


@login_required
def copier_reservation_dans_historique(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, proprietaire=request.user)
    HistoriqueReservation.objects.create(
        proprietaire=reservation.proprietaire,
        nom_client=reservation.nom_client,
        prenom_client=reservation.prenom_client,
        date_arrivee=reservation.date_arrivee,
        date_depart=reservation.date_depart,
        adulte_suplementaire=reservation.adulte_suplementaire,
        enfant_suplementaire=reservation.enfant_suplementaire,
        paiement_anticipe=reservation.paiement_anticipe,
        frais_suplementaire=reservation.frais_suplementaire,
        chambre=reservation.chambre,
        statut=reservation.statut,
        note=reservation.note,
        numero_facture=reservation.numero_facture
    )
    reservation.delete()
    return redirect('planning')

@login_required
def liste_historique_reservations(request):
    historique_reservations = HistoriqueReservation.objects.filter(proprietaire=request.user)
    context = {
        'historique_reservations': historique_reservations
    }
    return render(request, 'reservation/historique_reservations.html', context)

from django.utils.dateparse import parse_date
from datetime import datetime, timedelta
from chambre.models import Chambre, TypeChambre


def planning(request):
    # Récupération des chambres et réservations pour l'utilisateur connecté
    chambres = Chambre.objects.filter(proprietaire=request.user)
    reservations = Reservation.objects.filter(proprietaire=request.user)
    
    # Récupérer les paramètres GET
    debut = request.GET.get('debut')
    fin = request.GET.get('fin')
    search = request.GET.get('search', '').strip()
    type_chambre_id = request.GET.get('type_chambre')

    # Filtrer par dates si elles sont fournies
    if debut and fin:
        start_date = parse_date(debut)
        end_date = parse_date(fin)
        reservations = reservations.filter(date_arrivee__lte=end_date, date_depart__gte=start_date)
    else:
        start_date = datetime.now().replace(year=datetime.now().year - 2, month=1, day=1)
        end_date = start_date.replace(year=start_date.year + 5)

    # Filtrer par nom ou prénom si un terme de recherche est fourni
    if search:
        reservations = reservations.filter(
            nom_client__icontains=search
        ) | reservations.filter(
            prenom_client__icontains=search
        )

    # Filtrer les chambres par type de chambre si un type est sélectionné
    if type_chambre_id:
        chambres = chambres.filter(type_chambre__id=type_chambre_id)

    # Créer une liste de dates uniques pour l'intervalle spécifié
    dates_uniques = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

    # Préparer les données de planning
    planning_data = []
    for chambre in chambres:
        chambre_data = {
            'numero_chambre': chambre.numero_chambre,
            'prix': chambre.prix,
            'reservations': [],
        }
        for date in dates_uniques:
            reservation = reservations.filter(chambre=chambre, date_arrivee__lte=date, date_depart__gte=date).first()
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

    # Trouver la date de la dernière réservation pour faire défiler automatiquement jusqu'à cette date
    last_reservation = reservations.order_by('-date_depart').first()
    last_reservation_date = last_reservation.date_depart if last_reservation else datetime.now().date()
    
    # Récupérer tous les types de chambre pour le filtre
    types_chambre = TypeChambre.objects.filter(proprietaire=request.user)

    context = {
        'planning_data': planning_data,
        'dates_uniques': dates_uniques,
        'last_reservation_date': last_reservation_date,
        'debut': debut,
        'fin': fin,
        'search': search,
        'types_chambre': types_chambre,
        'selected_type_chambre': type_chambre_id,
    }
    return render(request, 'reservation/planning.html', context)
