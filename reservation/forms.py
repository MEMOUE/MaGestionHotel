from django import forms

from reservation.models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            'nom_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'prenom_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prenom du client'}),
            'adresse_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adresse du client'}),
            'date_arrivee': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date d\'arrivée'}),
            'date_reservation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de reservation'}),
            'nombre_jours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de jours'}),
            'chambre': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Chambre choisie'}),
            'etat': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Etat choisie'}),
            'statut': forms.Select(attrs={'class': 'form-control','placeholder': 'statut choisie' }),
        }
        error_messages = {
            'date_reservation': {
                'required': "Veuillez fournir une date de reservation.",
                'invalid': "Veuillez fournir une date valide pour la reservation.",
            },
            'date_arrivee': {
                'required': "Veuillez fournir une date d'arrivée.",
                'invalid': "Veuillez fournir une date valide pour l'arrivée.",
            },
            'nombre_jours': {
                'required': "Veuillez fournir le nombre de jours.",
                'invalid': "Veuillez fournir un nombre valide pour les jours.",
            },
            'etat': {
                'required': "Veuillez l'etat de la reservation .",
                'invalid': "Veuillez fournir un nombre valide pour les jours.",
            },
            'statut': {
                'required': 'Veuillez sélectionner un statut.',
            },
        }