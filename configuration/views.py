from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from configuration.forms import ConfigForm, ReglePrixForm
from configuration.models import Configuration, Categories


def home_config(request):
    return render(request, "confighotel/home.html")


def regle_prix(request):
    form = ReglePrixForm()
    if request.method == "POST":
        form = ReglePrixForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("confighotel:home-config")
    return render(request, "confighotel/create_rules.html", context={"form": form})


def update_rule(request, id):
    obj = get_object_or_404(Categories, id=id)
    if request.method == "POST":
        form = ReglePrixForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect("confighotel:list-rule")
    else:
        form = ReglePrixForm(instance=obj)
    return render(request, "confighotel/update_rule.html", {"form": form})


def delete_rule(request, id):
    regle = get_object_or_404(Categories, id=id)
    if request.method == "POST":
        regle.delete()
        return redirect("confighotel:list-rule")
    return render(request, "confighotel/delete_rule.html")


class CreateConfig(LoginRequiredMixin, CreateView):
    form_class = ConfigForm
    template_name = "confighotel/add.html"
    success_url = reverse_lazy("confighotel:home-config")

    def form_valid(self, form):
        form.instance.proprietaire = self.request.user
        return super().form_valid(form)

    def get_queryset(self):
        return Configuration.objects.filter(proprietaire=self.request.user)


class ListConfig(LoginRequiredMixin, ListView):
    template_name = "confighotel/list_config.html"

    def get_queryset(self):
        return Configuration.objects.filter(proprietaire=self.request.user)


class ListRegle(LoginRequiredMixin, ListView):
    template_name = "confighotel/list_regle.html"

    def get_queryset(self):
        # Filtrer les catégories par l'utilisateur connecté
        return Categories.objects.filter(proprietaire=self.request.user)


class DetailConfig(LoginRequiredMixin, DetailView):
    template_name = "confighotel/detail_config.html"

    def get_queryset(self):
        return Configuration.objects.filter(proprietaire=self.request.user)


class UpdateConfig(LoginRequiredMixin, UpdateView):
    form_class = ConfigForm
    template_name = "confighotel/add.html"

    def get_queryset(self):
        return Configuration.objects.filter(proprietaire=self.request.user)

    def form_valid(self, form):
        form.instance.proprietaire = self.request.user
        return super().form_valid(form)


def update_config(request):
    last = Configuration.objects.all().count()
    obj = Configuration.objects.get(id=last)
    form = ConfigForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("confighotel:detail-config")
    return render(request, "confighotel/add.html", {"form": form})


def header(request):
    conf = Configuration.objects.filter(proprietaire=request.user).first()  # Utilisez .first() pour obtenir un seul objet
    context = {'config': conf}  # Utilisez la clé 'configuration' au lieu de 'conf'
    return render(request, 'header.html', context)  # Passez le dictionnaire contexte
