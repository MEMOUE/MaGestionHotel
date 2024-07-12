from django import forms
from .models import Chambre, TypeChambre



class ChambreForm(forms.ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(ChambreForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['type_chambre'].queryset = TypeChambre.objects.filter(proprietaire=user)

    class Meta:
        model = Chambre
        exclude = ['proprietaire']
        labels = {
            'numero_chambre': 'Numéro de chambre',
            'type_chambre': 'Type de chambre',
            'prix': 'Prix',
            'date': 'Date',
        }
        widgets = {
            'numero_chambre': forms.TextInput(attrs={'class': 'form-control mx-auto', 'style': 'width: 50%;', 'placeholder': 'Entrez le numéro de chambre'}),
            'type_chambre': forms.Select(attrs={'class': 'form-control mx-auto', 'style': 'width: 50%;'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control mx-auto', 'style': 'width: 50%;', 'placeholder': 'Entrez le prix'}),
            'date': forms.DateInput(attrs={'class': 'form-control mx-auto', 'style': 'width: 50%;', 'type': 'date'}),
        }
        error_messages = {
            'numero_chambre': {
                'required': 'Veuillez fournir un numéro de chambre.',
            },
            'type_chambre': {
                'required': 'Veuillez sélectionner un type de chambre.',
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
        labels = {
            'typechambre': 'Type de chambre',
            'description': 'Description',
        }
        widgets = {
            'typechambre': forms.TextInput(attrs={'class': 'form-control mx-auto', 'style': 'width: 50%;', 'placeholder': 'Type de chambre'}),
            'description': forms.Textarea(attrs={'class': 'form-control mx-auto', 'style': 'width: 50%;', 'rows': 3, 'placeholder': 'Description'}),
        }
        error_messages = {
            'typechambre': {
                'required': 'Veuillez fournir un type de chambre.',
            },
            'description': {
                'required': 'Veuillez fournir une description.',
            },
        }
