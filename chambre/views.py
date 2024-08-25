from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ChambreForm
from .models import Chambre
from .models import TypeChambre
from .forms import TypeChambreForm

@login_required
def chambre_view(request):
    if request.method == 'POST':
        form = ChambreForm(user=request.user, data=request.POST)
        if form.is_valid():
            chambre = form.save(commit=False)
            chambre.proprietaire = request.user
            chambre.save()
            return redirect('liste_chambre')
    else:
        form = ChambreForm(user=request.user)  # Pass request.user as 'user' argument
    return render(request, 'chambre/chambre.html', {'form': form})


def liste_chambre(request):
    # Récupérer les chambres associées à l'utilisateur connecté
    chambres = Chambre.objects.filter(proprietaire=request.user)
    return render(request, 'chambre/liste_chambre.html', {'chambres': chambres})


def modifier_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == 'POST':
        print("Données POST : ", request.POST)  # Affiche les données POST
        # Passez user via kwargs uniquement
        form = ChambreForm(data=request.POST, instance=chambre, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('liste_chambre')
        else:
            print("Formulaire non valide : ", form.errors)
    else:
        form = ChambreForm(instance=chambre, user=request.user)

    return render(request, 'chambre/modifier_chambre.html', {'form': form, 'chambre': chambre})


def supprimer_chambre(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == 'POST':
        chambre.delete()
        return redirect('liste_chambres')

    return render(request, 'chambre/supprimer_chambre.html', {'chambre': chambre})


@login_required
def typechambre_list(request):
    types = TypeChambre.objects.filter(proprietaire=request.user)
    return render(request, 'chambre/typechambre_list.html', {'types': types})

@login_required
def typechambre_new(request):
    if request.method == "POST":
        form = TypeChambreForm(request.POST)
        if form.is_valid():
            typechambre = form.save(commit=False)
            typechambre.proprietaire = request.user
            typechambre.save()
            return redirect('typechambre_list')
    else:
        form = TypeChambreForm()
    return render(request, 'chambre/typechambre_new.html', {'form': form})

@login_required
def typechambre_edit(request, pk):
    typechambre = get_object_or_404(TypeChambre, pk=pk)
    if request.method == "POST":
        form = TypeChambreForm(request.POST, instance=typechambre)
        if form.is_valid():
            typechambre = form.save(commit=False)
            typechambre.proprietaire = request.user
            typechambre.save()
            return redirect('typechambre_list')
    else:
        form = TypeChambreForm(instance=typechambre)
    return render(request, 'chambre/typechambre_edit.html', {'form': form})

@login_required
def typechambre_delete(request, pk):
    typechambre = get_object_or_404(TypeChambre, pk=pk)
    if request.method == "POST":
        typechambre.delete()
        return redirect('typechambre_list')
    return render(request, 'chambre/typechambre_delete.html', {'typechambre': typechambre})