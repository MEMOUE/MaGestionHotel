from .models import Chambre
from django import forms
from .models import TypeChambre

class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        exclude = ['proprietaire']  # Exclure le champ proprietaire du formulaire
        labels = {
            'numero_chambre': 'Numéro de chambre',
            'type_chambre': 'Type de chambre',
            'statut': 'Statut',
            'prix': 'Prix',
            'date': 'Date',
            'etat': 'Etat'
        }
        widgets = {
            'numero_chambre': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px'}),
            'type_chambre': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px'}),
            'statut': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 300px'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'style': 'width: 300px'}),
            'etat': forms.Select(attrs={'class': 'form-control', 'style': 'width: 300px'}),
        }
        error_messages = {
            'numero_chambre': {
                'required': 'Veuillez fournir un numéro de chambre.',
            },
            'type_chambre': {
                'required': 'Veuillez sélectionner un type de chambre.',
            },
            'statut': {
                'required': 'Veuillez sélectionner un statut.',
            },
            'prix': {
                'required': 'Veuillez fournir un prix.',
                'invalid': 'Veuillez fournir un prix valide.',
            },
            'date': {
                'required': 'Veuillez fournir une date.',
                'invalid': 'Veuillez fournir une date valide.',
            },
        }


class TypeChambreForm(forms.ModelForm):
    class Meta:
        model = TypeChambre
        fields = ['typechambre', 'description']
        widgets = {
            'typechambre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type de chambre'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }