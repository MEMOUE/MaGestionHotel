from django.shortcuts import render

# Create your views here.

def home_paiement(request):
    plans = [
        { 'duration': 3, 'title': 'Abonnement de 3 mois', 'description': 'Description des fonctionnalités incluses...', 'price': 50, 'link': '/payment?duration=3' },
        { 'duration': 6, 'title': 'Abonnement de 6 mois', 'description': 'Description des fonctionnalités incluses...', 'price': 90, 'link': '/payment?duration=6' },
        { 'duration': 9, 'title': 'Abonnement de 9 mois', 'description': 'Description des fonctionnalités incluses...', 'price': 135, 'link': '/payment?duration=9' },
        { 'duration': 12, 'title': 'Abonnement de 12 mois', 'description': 'Description des fonctionnalités incluses...', 'price': 180, 'link': '/payment?duration=12' }
        # Ajoutez d'autres plans ici si nécessaire
    ]
    return render(request, "paiement/home.html", {'plans': plans})




