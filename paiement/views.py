from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import AutreRevenuCout
from .forms import AutreRevenuCoutForm

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

@login_required
def autre_revenu_cout_list(request):
    revenus_couts = AutreRevenuCout.objects.filter(proprietaire=request.user)
    return render(request, 'paiement/autre_revenu_cout_list.html', {'revenus_couts': revenus_couts})

@login_required
def autre_revenu_cout_create(request):
    if request.method == 'POST':
        form = AutreRevenuCoutForm(request.POST)
        if form.is_valid():
            revenu_cout = form.save(commit=False)
            revenu_cout.proprietaire = request.user
            revenu_cout.save()
            return redirect('autre_revenu_cout_list')
    else:
        form = AutreRevenuCoutForm()
    return render(request, 'paiement/autre_revenu_cout_form.html', {'form': form})

@login_required
def autre_revenu_cout_update(request, pk):
    revenu_cout = get_object_or_404(AutreRevenuCout, pk=pk, proprietaire=request.user)
    if request.method == 'POST':
        form = AutreRevenuCoutForm(request.POST, instance=revenu_cout)
        if form.is_valid():
            form.save()
            return redirect('autre_revenu_cout_list')
    else:
        form = AutreRevenuCoutForm(instance=revenu_cout)
    return render(request, 'paiement/autre_revenu_cout_form.html', {'form': form})

@login_required
def autre_revenu_cout_delete(request, pk):
    revenu_cout = get_object_or_404(AutreRevenuCout, pk=pk, proprietaire=request.user)
    if request.method == 'POST':
        revenu_cout.delete()
        return redirect('autre_revenu_cout_list')
    return render(request, 'paiement/autre_revenu_cout_confirm_delete.html', {'revenu_cout': revenu_cout})
