from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users, SecondaryUser
#from captcha.fields import ReCaptchaField





class InscriptionForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ("username", "email", "first_name", "last_name",)

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Nom d'utilisateur"}),
            "email": forms.EmailInput(attrs={"class": "form-control custom-input", "placeholder": "Adresse e-mail"}),
            "first_name": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Nom"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Mot de passe"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Confirmer le mot de passe"}),
        }




class ConnexionForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur", widget=forms.TextInput(attrs={"class": "form-control custom-input", "placeholder": "Nom d'utilisateur"}))
    password = forms.CharField(max_length=100, label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control custom-input", "placeholder": "Mot de passe"}))
    #captcha = ReCaptchaField()


from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import SecondaryUser

class SecondaryUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = SecondaryUser
        fields = ('username', 'password', 'nom', 'prenom',
                  'can_access_chambres', 'can_access_resto', 'can_access_configuration',
                  'can_access_reservation', 'can_access_paiements', 'can_access_statistics',
                  'can_access_history', 'can_access_settings')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.hashed_password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class SecondaryUserUpdateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = SecondaryUser
        fields = ('username', 'password', 'nom', 'prenom',
                  'can_access_chambres', 'can_access_resto', 'can_access_configuration',
                  'can_access_reservation', 'can_access_paiements', 'can_access_statistics',
                  'can_access_history', 'can_access_settings')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        return None

class SecondaryUserLoginForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            try:
                user = SecondaryUser.objects.get(username=username)
                if not check_password(password, user.hashed_password):
                    raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect")
            except SecondaryUser.DoesNotExist:
                raise forms.ValidationError("Nom d'utilisateur ou mot de passe incorrect")

        return cleaned_data
