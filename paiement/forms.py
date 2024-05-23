from django import forms
from .models import AutreRevenuCout

class AutreRevenuCoutForm(forms.ModelForm):
    class Meta:
        model = AutreRevenuCout
        fields = ['temps', 'type', 'montant', 'note']
        widgets = {
            'temps': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note', 'rows': 3}),
        }
