from django import forms

from resto.models import Restaurant


class RestoForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude = ['proprietaire']
        fields = "__all__"

        widgets = {
            'nom_menu': forms.TextInput(attrs={'class': 'form-control orange-input', 'placeholder': 'Nom du menu'}),
            'type': forms.Select(attrs={'class': 'form-select orange-input', 'placeholder': 'Type de menu'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control green-input', 'placeholder': 'Quantité'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control white-input'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control white-input', 'placeholder': 'Prix'}),
            'date': forms.DateInput(attrs={'class': 'form-control white-input', 'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super(RestoForm, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control white-input'