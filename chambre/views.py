from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChambreForm
from .models import Chambre

def chambre_view(request):
    if request.method == 'POST':
        form = ChambreForm(request.POST)
        if form.is_valid():
            # Modifiez la logique pour associer la chambre à l'utilisateur connecté
            chambre = form.save(commit=False)
            chambre.proprietaire = request.user  # Associe la chambre à l'utilisateur connecté
            chambre.save()
            return redirect('liste_chambre')
    else:
        form = ChambreForm()
    return render(request, 'chambre/chambre.html', {'form': form})

def liste_chambre(request):
    # Récupérer les chambres associées à l'utilisateur connecté
    chambres = Chambre.objects.filter(proprietaire=request.user)
    return render(request, 'chambre/liste_chambre.html', {'chambres': chambres})


def modifier_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == 'POST':
        form = ChambreForm(request.POST, instance=chambre)
        if form.is_valid():
            form.save()
            return redirect('liste_chambre')
    else:
        form = ChambreForm(instance=chambre)

    return render(request, 'chambre/modifier_chambre.html', {'form': form, 'chambre': chambre})

def supprimer_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == 'POST':
        chambre.delete()
        return redirect('liste_chambres')

    return render(request, 'chambre/supprimer_chambre.html', {'chambre': chambre})