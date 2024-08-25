from django import forms
from .models import AutreRevenuCout

class AutreRevenuCoutForm(forms.ModelForm):
    class Meta:
        model = AutreRevenuCout
        fields = ['type', 'montant', 'note']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),  # Use Select widget for choices field
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Note', 'rows': 3}),
        }


from .models import Subscription

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['duration']
        widgets = {
            'duration': forms.RadioSelect
        }
