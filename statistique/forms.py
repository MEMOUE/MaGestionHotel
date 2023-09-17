from django import forms
from .models import Statistique


class Statistiqueform(forms.Form):
    class Meta:
        model = Statistique
        fields = "__all__"
        widgets = {
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': ' date de debut'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': ' date de fin'}),

        }


