from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from reservation.models import Reservation
from resto.form import RestoForm, CommandeForm
from resto.models import Restaurant,Commande
from django.urls import reverse_lazy


class CreateMenu(CreateView):
    form_class = RestoForm
    template_name = "resto/add_menu.html"
    success_url = "/resto/home-resto"

    def form_valid(self, form):
        # Récupérer l'utilisateur connecté
        user = self.request.user
        # Associer l'utilisateur au menu avant de le sauvegarder
        form.instance.proprietaire = user
        return super().form_valid(form)

class ListMenu(LoginRequiredMixin, ListView):
    template_name = "resto/home_resto.html"
    model = Restaurant

    def get_queryset(self):
        user = self.request.user
        return Restaurant.objects.filter(proprietaire=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menus'] = context['object_list']
        return context

class UpdateMenu(UpdateView):
    form_class = RestoForm
    template_name = "resto/add_menu.html"
    success_url = reverse_lazy("home-resto")

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Restaurant, id=id)


class DeleteMenu(DeleteView):
    template_name = "resto/delete.html"
    queryset = Restaurant.objects.all()
    success_url = reverse_lazy("home-resto")

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Restaurant, id=id)


def deleteMenu(request, id):
    obj = Restaurant.objects.get(id=id)
    # Faire ce que vous avez à faire avec l'objet 'obj'
    pass



def gestion_commande(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    commandes = Commande.objects.filter(reservation=reservation)

    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            commande = form.save(commit=False)
            commande.reservation = reservation
            commande.save()
            return redirect('gestion_commande', reservation_id=reservation.id)
    else:
        form = CommandeForm()

    return render(request, 'resto/gestion_commande.html', {
        'reservation': reservation,
        'commandes': commandes,
        'form': form,
    })

def modifier_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    if request.method == 'POST':
        form = CommandeForm(request.POST, instance=commande)
        if form.is_valid():
            form.save()
            return redirect('gestion_commande', reservation_id=commande.reservation.id)
    else:
        form = CommandeForm(instance=commande)

    return render(request, 'resto/modifier_commande.html', {
        'form': form,
        'commande': commande,
    })

def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    reservation_id = commande.reservation.id
    commande.delete()
    return redirect('gestion_commande', reservation_id=reservation_id)
