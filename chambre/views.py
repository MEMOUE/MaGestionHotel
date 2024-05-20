from django.shortcuts import render, redirect, get_object_or_404
from .forms import ChambreForm
from .models import Chambre
from .models import TypeChambre
from .forms import TypeChambreForm

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


def typechambre_list(request):
    types = TypeChambre.objects.all()
    return render(request, 'chambre/typechambre_list.html', {'types': types})

def typechambre_new(request):
    if request.method == "POST":
        form = TypeChambreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('typechambre_list')
    else:
        form = TypeChambreForm()
    return render(request, 'chambre/typechambre_new.html', {'form': form})

def typechambre_edit(request, pk):
    typechambre = get_object_or_404(TypeChambre, pk=pk)
    if request.method == "POST":
        form = TypeChambreForm(request.POST, instance=typechambre)
        if form.is_valid():
            form.save()
            return redirect('typechambre_list')
    else:
        form = TypeChambreForm(instance=typechambre)
    return render(request, 'chambre/typechambre_edit.html', {'form': form})

def typechambre_delete(request, pk):
    typechambre = get_object_or_404(TypeChambre, pk=pk)
    if request.method == "POST":
        typechambre.delete()
        return redirect('typechambre_list')
    return render(request, 'chambre/typechambre_delete.html', {'typechambre': typechambre})
