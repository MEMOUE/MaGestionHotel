from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm, ConnexionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SecondaryUserCreationForm, SecondaryUserUpdateForm
from .models import SecondaryUser
from .forms import ConnexionForm
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.http import HttpResponse
from django.contrib.auth import get_user_model



User = get_user_model()

def inscription(request):
    form = InscriptionForm()

    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verification_token = get_random_string(length=64)
            user.is_active = False  # Désactiver l'utilisateur jusqu'à ce que l'email soit vérifié
            user.save()

            # Envoyer l'email de vérification
            verification_url = reverse('verify_email', args=[user.email_verification_token])
            full_url = f"{settings.SITE_URL}{verification_url}"
            send_mail(
                'Verify your email address',
                f'Please click the following link to verify your email: {full_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Votre compte a été créé avec succès. Veuillez vérifier votre email pour l'activer.")
            return redirect("inscription")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ {field}: {error}")

    return render(request, "users/inscription.html", context={"form": form})



User = get_user_model()

def verify_email(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    user.email_verified = True
    user.email_verification_token = None
    user.is_active = True  # Activer l'utilisateur après la vérification
    user.save()
    return HttpResponse('Email vérifié avec succès! Vous pouvez maintenant vous connecter.')



def connexion(request):
    form = ConnexionForm()

    if request.method == "POST":
        form = ConnexionForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    if user.email_verified:
                        login(request, user)
                        if user.is_staff:
                            return redirect("admin:index")
                        else:
                            return redirect("home-users")
                    else:
                        messages.error(request, "Veuillez vérifier votre email avant de vous connecter.")
                else:
                    messages.error(request, "Votre compte est désactivé.")
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erreur dans le champ {field}: {error}")

    return render(request, "index.html", {"form": form})



from reservation.models import Reservation
from chambre.models import Chambre
from datetime import date
from django.utils.timezone import now

@login_required
def home(request):
    user = request.user
    
    # Calcul des réservations en cours de l'utilisateur connecté
    enregistrements_en_cours = Reservation.objects.filter(proprietaire=user, statut='confirmée').count()
    
    # Calcul des chambres disponibles pour l'utilisateur connecté
    chambres_totales = Chambre.objects.filter(proprietaire=user).count()
    chambres_occupees = Reservation.objects.filter(chambre__proprietaire=user, statut='confirmée').values_list('chambre', flat=True).distinct().count()
    chambres_disponibles = chambres_totales - chambres_occupees
    
    # Calcul des enregistrements du jour de l'utilisateur connecté
    enregistrements_du_jour = Reservation.objects.filter(proprietaire=user, date_arrivee=now().date()).count()
    
    # Calcul des départs du jour de l'utilisateur connecté
    departs_du_jour = Reservation.objects.filter(proprietaire=user, date_depart=now().date()).count()
    
    context = {
        "user": user,
        "enregistrements_en_cours": enregistrements_en_cours,
        "chambres_disponibles": chambres_disponibles,
        "enregistrements_du_jour": enregistrements_du_jour,
        "departs_du_jour": departs_du_jour,
    }
    return render(request, "users/accueil.html", context)
#@login_required
#def index(request):
#    return render(request, "index.html")


def menusysteme(request):
    return render(request, "users/menusysteme.html")


@login_required
def deconnexion(request):
    logout(request)
    return redirect("index")



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SecondaryUser
from .forms import SecondaryUserCreationForm, SecondaryUserUpdateForm, SecondaryUserLoginForm

@login_required
def create_secondary_user(request):
    if request.method == 'POST':
        form = SecondaryUserCreationForm(request.POST)
        if form.is_valid():
            secondary_user = form.save(commit=False)
            secondary_user.proprietaire = request.user
            secondary_user.save()
            messages.success(request, 'Utilisateur secondaire créé avec succès.')
            return redirect('list_secondary_users')
    else:
        form = SecondaryUserCreationForm()
    return render(request, 'users/create_secondary_user.html', {'form': form})


@login_required
def update_secondary_user(request, user_id):
    secondary_user = get_object_or_404(SecondaryUser, id=user_id, proprietaire=request.user)
    if request.method == 'POST':
        form = SecondaryUserUpdateForm(request.POST, instance=secondary_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur secondaire mis à jour avec succès.')
            return redirect('list_secondary_users')
    else:
        form = SecondaryUserUpdateForm(instance=secondary_user)
    return render(request, 'users/update_secondary_user.html', {'form': form})

@login_required
def delete_secondary_user(request, user_id):
    secondary_user = get_object_or_404(SecondaryUser, id=user_id, proprietaire=request.user)
    if request.method == 'POST':
        secondary_user.delete()
        messages.success(request, 'Utilisateur secondaire supprimé avec succès.')
        return redirect('list_secondary_users')
    return render(request, 'users/delete_secondary_user.html', {'secondary_user': secondary_user})

@login_required
def list_secondary_users(request):
    secondary_users = SecondaryUser.objects.filter(proprietaire=request.user)
    return render(request, 'users/list_secondary_users.html', {'secondary_users': secondary_users})


def secondary_user_login(request):
    if request.method == 'POST':
        form = SecondaryUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = SecondaryUser.objects.get(username=username)
            login(request, user)
            return redirect('home')  # Redirige vers la page d'accueil ou une autre vue appropriée
    else:
        form = SecondaryUserLoginForm()
    return render(request, 'users/secondary_user_login.html', {'form': form})


#erreur
from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    return render(request, 'errors/404.html', {})

def custom_error_view(request):
    return render(request, 'errors/500.html', {})

def custom_permission_denied_view(request, exception):
    return render(request, 'errors/403.html', {})

def custom_bad_request_view(request, exception):
    return render(request, 'errors/400.html', {})
