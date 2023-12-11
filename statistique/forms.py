from django import forms
from .models import Statistique

class StatistiqueForm(forms.ModelForm):
    class Meta:
        model = Statistique
        fields = "__all__"
        widgets = {
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
