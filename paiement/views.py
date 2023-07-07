from django.shortcuts import render

# Create your views here.


def home_paiement(request):
    return render(request, "paiement/home.html")