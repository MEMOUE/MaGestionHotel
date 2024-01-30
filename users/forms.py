from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


class InscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email", "first_name", "last_name",)

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Nom d'utilisateur"}),
            "email": forms.EmailInput(attrs={"class": "form-control custom-input", "placeholder": "Adresse e-mail"}),
            "first_name": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Nom"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Mot de passe"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Confirmer le mot de passe"}),
        }


class ConnexionForm(AuthenticationForm):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur", widget=forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Nom d'utilisateur"}))
    password = forms.CharField(max_length=100, label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Mot de passe"}))




