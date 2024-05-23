from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm, ConnexionForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import InscriptionForm

def inscription(request):
    form = InscriptionForm()

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès. Veuillez-vous connecter maintenant")
            return redirect("inscription")
        else:
            # Afficher des messages d'erreur pour chaque champ
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ {field}: {error}")

    return render(request, "users/inscription.html", context={"form": form})


def connexion(request):
    form = ConnexionForm()

    if request.method == "POST":
        form = ConnexionForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    if user.is_staff:
                        login(request, user)
                        return redirect("admin:index")
                    else:
                        login(request, user)
                        return redirect("home-users")
                else:
                    messages.error(request, "Votre compte est désactivé.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, "users/connexion.html", context={"form": form})



@login_required
def home(request):
    return render(request, "users/accueil.html")

#@login_required
#def index(request):
#    return render(request, "index.html")


def menusysteme(request):
    return render(request, "users/menusysteme.html")


@login_required
def deconnexion(request):
    logout(request)
    return redirect("index")
