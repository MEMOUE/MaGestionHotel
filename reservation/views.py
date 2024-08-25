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


@login_required
def details_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user != reservation.proprietaire:
        return HttpResponseForbidden("Vous n'avez pas la permission de voir les détails de cette réservation.")

    # Calculer le nombre de jours si nécessaire
    nombre_jours = (reservation.date_depart - reservation.date_arrivee).days if reservation.date_depart and reservation.date_arrivee else 0

    context = {
        'reservation': reservation,
        'nombre_jours': nombre_jours,
    }
    return render(request, 'reservation/details_reservation.html', context)


def supprimer_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        reservation.delete()
        return redirect('planning')

    return render(request, 'reservation/supprimer_reservation.html', {'reservation': reservation})
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.decorators import login_required
from reservation.models import Reservation
from resto.models import  Commande
from configuration.models import Configuration

@login_required
def genere_et_affiche_facture(request, reservation_id):
    try:
        reservation = get_object_or_404(Reservation, id=reservation_id, proprietaire=request.user)
        configuration = get_object_or_404(Configuration, proprietaire=request.user)

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Adjust margins and widths
        margin_left = 50
        margin_top = height - 50
        content_width = width - 2 * margin_left

        # Calculate total amount
        nombre_jours = (reservation.date_depart - reservation.date_arrivee).days if reservation.date_depart and reservation.date_arrivee else 0
        chambre_prix = Decimal(reservation.chambre.prix)
        paiement_anticipe = Decimal(reservation.paiement_anticipe)
        frais_suplementaire = Decimal(reservation.frais_suplementaire)
        remise = Decimal(reservation.remise) if reservation.remise else Decimal(0.0)  # Remise

        # Convert all prices to Decimal
        montant_total_commandes = Decimal(0.0)
        commandes = Commande.objects.filter(reservation=reservation, annulee=False)
        for commande in commandes:
            montant_total_commandes += Decimal(commande.prix_total)

        montant_total = (nombre_jours * chambre_prix) + frais_suplementaire + montant_total_commandes - paiement_anticipe - remise  # Adjusted total with remise

        # Invoice content
        p.setFont("Helvetica", 16)
        p.drawString(margin_left, margin_top, configuration.nom)
        p.setFont("Helvetica", 12)
        p.drawString(margin_left, margin_top - 20, f"Téléphone : {configuration.telephone}")
        p.drawString(margin_left, margin_top - 40, f"Adresse : {configuration.adresse}")

        facture_numero = reservation.numero_facture.split('-')[0] if '-' in reservation.numero_facture else reservation.numero_facture

        p.setFont("Helvetica-Bold", 16)
        p.drawString(margin_left, margin_top - 80, f"Facture N° {facture_numero}")
        p.line(margin_left, margin_top - 90, margin_left + content_width, margin_top - 90)

        # Client Information
        p.setFont("Helvetica", 12)
        p.drawString(margin_left, margin_top - 120, f"Nom : {reservation.nom_client}")
        p.drawString(margin_left, margin_top - 140, f"Prénom : {reservation.prenom_client}")
        p.drawString(margin_left, margin_top - 160, f"Téléphone : {reservation.telephone}")  # Téléphone du client
        p.drawString(margin_left, margin_top - 180, f"Date arrivée : {reservation.date_arrivee.strftime('%d-%m-%Y')}")
        p.drawString(margin_left, margin_top - 200, f"Date départ : {reservation.date_depart.strftime('%d-%m-%Y')}")
        p.drawString(margin_left, margin_top - 220, f"Chambre : {reservation.chambre.numero_chambre}")
        p.drawString(margin_left, margin_top - 240, f"Adultes supplémentaires : {reservation.adulte_suplementaire}")
        p.drawString(margin_left, margin_top - 260, f"Enfants supplémentaires : {reservation.enfant_suplementaire}")
        p.drawString(margin_left, margin_top - 280, f"Statut : {reservation.get_statut_display()}")
        p.drawString(margin_left, margin_top - 300, f"Note : {reservation.note}")
        p.drawString(margin_left, margin_top - 320, f"Paiement anticipé : {paiement_anticipe} FCFA")
        p.drawString(margin_left, margin_top - 340, f"Remise : {remise} FCFA")  # Remise

        # Commande Details
        if commandes.exists():
            p.setFont("Helvetica-Bold", 14)
            p.drawString(margin_left, margin_top - 380, "Détails des Commandes")
            p.line(margin_left, margin_top - 390, margin_left + content_width, margin_top - 390)
            p.setFont("Helvetica", 12)

            y_position = margin_top - 410
            for commande in commandes:
                p.drawString(margin_left, y_position, f"Plat : {commande.plat.nom_menu} - Quantité : {commande.quantite} - Prix Total : {commande.prix_total} FCFA")
                y_position -= 20

        # Montant total à payer
        p.setFont("Helvetica-Bold", 16)
        p.drawString(margin_left, y_position - 20, f"Montant total à payer : {montant_total} FCFA")
        p.line(margin_left, y_position - 30, margin_left + content_width, y_position - 30)

        # Date of Invoice Creation
        p.setFont("Helvetica", 10)
        temps = timezone.now()
        p.drawString(margin_left, 50, f"Fait le : {temps.day}-{temps.month}-{temps.year} à {temps.hour}h{temps.minute}min{temps.second}s")

        p.showPage()
        p.save()

        buffer.seek(0)

        # Provide options to download, print, and share
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="facture_{facture_numero}_{reservation.nom_client}.pdf"'

        return response

    except Exception as e:
        return HttpResponseBadRequest(f"Erreur lors de la génération de la facture : {str(e)}")


@login_required
def copier_reservation_dans_historique(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, proprietaire=request.user)
    
    # Copier les données dans l'historique
    HistoriqueReservation.objects.create(
        proprietaire=reservation.proprietaire,
        nom_client=reservation.nom_client,
        prenom_client=reservation.prenom_client,
        telephone=reservation.telephone,  # Ajout du champ téléphone
        date_arrivee=reservation.date_arrivee,
        date_depart=reservation.date_depart,
        adulte_suplementaire=reservation.adulte_suplementaire,
        enfant_suplementaire=reservation.enfant_suplementaire,
        paiement_anticipe=reservation.paiement_anticipe,
        frais_suplementaire=reservation.frais_suplementaire,
        remise=reservation.remise,  # Ajout du champ remise
        chambre=reservation.chambre,
        statut=reservation.statut,
        note=reservation.note,
        numero_facture=reservation.numero_facture
    )
    
    # Mettre à jour le statut de la réservation à "terminée" au lieu de la supprimer
    reservation.statut = 'terminée'  # Assurez-vous que 'terminee' est une option valide dans votre champ `statut`
    reservation.save()
    
    return redirect('planning')


@login_required
def liste_historique_reservations(request):
    historique_reservations = HistoriqueReservation.objects.filter(proprietaire=request.user)
    context = {
        'historique_reservations': historique_reservations
    }
    return render(request, 'reservation/historique_reservations.html', context)

from django.shortcuts import render
from chambre.models import Chambre, TypeChambre
from reservation.models import Reservation
from django.utils.dateparse import parse_date
from datetime import datetime, timedelta


def planning(request):
    # Récupération des chambres et réservations pour l'utilisateur connecté
    chambres = Chambre.objects.filter(proprietaire=request.user)
    reservations = Reservation.objects.filter(proprietaire=request.user)

    # Définir les dates par défaut
    today = datetime.now().date()
    debut = request.GET.get('debut', today.strftime('%Y-%m-%d'))
    fin = request.GET.get('fin', (today + timedelta(days=30)).strftime('%Y-%m-%d'))

    start_date = parse_date(debut)
    end_date = parse_date(fin)

    # Filtrer les réservations par dates
    reservations = reservations.filter(date_arrivee__lte=end_date, date_depart__gte=start_date)

    # Filtrer par nom ou prénom si un terme de recherche est fourni
    search = request.GET.get('search', '').strip()
    if search:
        reservations = reservations.filter(
            nom_client__icontains=search
        ) | reservations.filter(
            prenom_client__icontains=search
        )

    # Filtrer les chambres par type de chambre si un type est sélectionné
    type_chambre_id = request.GET.get('type_chambre')
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
                    'nombre_jours': (
                                reservation.date_depart - reservation.date_arrivee).days if reservation.date_depart and reservation.date_arrivee else '',
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
    last_reservation_date = last_reservation.date_depart if last_reservation else today

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

