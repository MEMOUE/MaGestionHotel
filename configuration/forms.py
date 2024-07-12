from django import forms
from configuration.models import Configuration

class ConfigForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['proprietaire']
        fields = "__all__"

        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control w-100"}),
            "telephone": forms.TextInput(attrs={"class": "form-control w-100"}),
            "adresse": forms.TextInput(attrs={"class": "form-control w-100"})
        }


from .models import PricingRule

class PricingRuleForm(forms.ModelForm):
    class Meta:
        model = PricingRule
        fields = [
            'prix', 'date_heure_arrivee', 'date_heure_depart',
            'tarif_supplementaire_adulte', 'tarif_supplementaire_enfant', 'frais_supplementaire'
        ]
        widgets = {
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_heure_arrivee': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'date_heure_depart': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tarif_supplementaire_adulte': forms.NumberInput(attrs={'class': 'form-control'}),
            'tarif_supplementaire_enfant': forms.NumberInput(attrs={'class': 'form-control'}),
            'frais_supplementaire': forms.NumberInput(attrs={'class': 'form-control'}),
        }
