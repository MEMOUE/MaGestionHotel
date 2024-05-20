from django import forms

from configuration.models import Configuration, Categories


class ConfigForm(forms.ModelForm):
    class Meta:
        model = Configuration
        exclude = ['proprietaire']
        fields = "__all__"

        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control m-2"}),
            "telephone": forms.TextInput(attrs={"class": "form-control m-2"}),
            "adresse": forms.TextInput(attrs={"class": "form-control m-2"})
        }


class ReglePrixForm(forms.ModelForm):
    class Meta:
        model = Categories
        exclude = ['proprietaire']
        fields = "__all__"

        widgets = {
            "categorie": forms.Select(attrs={"class": "form-select m-2"}),
            "prix_enfant": forms.NumberInput(attrs={"class": "form-control m-2"}),
            "prix_adulte": forms.NumberInput(attrs={"class": "form-control m-2"})
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
