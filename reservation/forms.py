# forms.py

from django import forms
from .models import Reservation
from chambre.models import Chambre

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        exclude = ['proprietaire', 'numero_facture']
        fields = "__all__"
        widgets = {
            'nom_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du client'}),
            'prenom_client': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom du client'}),
            'date_arrivee': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date d\'arrivée'}),
            'date_depart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date de départ'}),
            'adulte_suplementaire': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Adulte supplémentaire'}),
            'enfant_suplementaire': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enfant supplémentaire'}),
            'paiement_anticipe': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paiement anticipé'}),
            'frais_suplementaire':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Frais supplémentaires'}),
            'chambre': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Chambre choisie'}),
            'statut': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Statut'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Notes', 'rows': 2, 'cols': 30}),
        }
        error_messages = {
            'date_arrivee': {
                'required': "Veuillez fournir une date d'arrivée.",
                'invalid': "Veuillez fournir une date d'arrivée valide.",
            },
            'date_depart': {
                'required': "Veuillez fournir une date de départ.",
                'invalid': "Veuillez fournir une date de départ valide.",
            },
            'adulte_suplementaire': {
                'invalid': "Veuillez fournir un nombre valide pour les adultes supplémentaires.",
            },
            'enfant_suplementaire': {
                'invalid': "Veuillez fournir un nombre valide pour les enfants supplémentaires.",
            },
            'paiement_anticipe': {
                'invalid': "Veuillez fournir un montant valide pour le paiement anticipé.",
            },
            'frais_suplementaire': {
                'invalid': "Veuillez fournir un montant valide pour les frais supplémentaires.",
            },
            'chambre': {
                'required': "Veuillez sélectionner une chambre.",
            },
            'statut': {
                'required': 'Veuillez sélectionner un statut.',
            },
        }

    def __init__(self, user, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['chambre'].queryset = Chambre.objects.filter(proprietaire=user)
