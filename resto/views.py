from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from resto.form import RestoForm
from resto.models import Restaurant
from django.urls import reverse_lazy


class CreateMenu(CreateView):
    form_class = RestoForm
    template_name = "resto/add_menu.html"
    success_url = "/resto"


class ListMenu(LoginRequiredMixin, ListView):
    template_name = "resto/home_resto.html"
    model = Restaurant

    def get_queryset(self):
        return Restaurant.objects.filter(proprietaire=self.request.user)


class UpdateMenu(UpdateView):
    form_class = RestoForm
    template_name = "resto/add_menu.html"
    success_url = reverse_lazy("resto:list_menu")

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Restaurant, id=id)


class DeleteMenu(DeleteView):
    template_name = "resto/delete.html"
    queryset = Restaurant.objects.all()
    success_url = reverse_lazy("resto:list_menu")

    def get_object(self):
        id = self.kwargs.get("id")
        return get_object_or_404(Restaurant, id=id)


def deleteMenu(request, id):
    obj = Restaurant.objects.get(id=id)
    # Faire ce que vous avez à faire avec l'objet 'obj'
    pass
