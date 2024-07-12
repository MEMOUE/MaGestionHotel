from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from configuration.forms import ConfigForm
from configuration.models import Configuration
from django.contrib import messages


def home_config(request):
    return render(request, "confighotel/home.html")

class CreateConfig(LoginRequiredMixin, CreateView):
    form_class = ConfigForm
    template_name = "confighotel/add.html"
    success_url = reverse_lazy("home-config")

    def dispatch(self, request, *args, **kwargs):
        # Vérifiez si l'utilisateur a déjà une configuration
        if Configuration.objects.filter(proprietaire=request.user).exists():
            messages.error(request, "Vous avez déjà une configuration.")
            config = Configuration.objects.get(proprietaire=request.user)
            return redirect("detail-config", pk=config.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.proprietaire = self.request.user
        messages.success(self.request, "Configuration créée avec succès.")
        return super().form_valid(form)

    def get_queryset(self):
        return Configuration.objects.filter(proprietaire=self.request.user)

class ListConfig(LoginRequiredMixin, ListView):
    template_name = "confighotel/list_config.html"

    def get_queryset(self):
        return Configuration.objects.filter(proprietaire=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_config'] = Configuration.objects.filter(proprietaire=self.request.user).exists()
        return context

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
        messages.success(self.request, "Configuration mise à jour avec succès.")
        return super().form_valid(form)

def update_config(request):
    last = Configuration.objects.all().count()
    obj = Configuration.objects.get(id=last)
    form = ConfigForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Configuration mise à jour avec succès.")
        return redirect('list-config')
    return render(request, "confighotel/add.html", {"form": form})

@login_required
def delete_config(request, pk):
    config = get_object_or_404(Configuration, pk=pk, proprietaire=request.user)
    if request.method == 'POST':
        config.delete()
        messages.success(request, "Configuration supprimée avec succès.")
        return redirect('list-config')
    return render(request, 'confighotel/confirm_delete.html', {'config': config})

def header(request):
    conf = Configuration.objects.filter(proprietaire=request.user).first()
    context = {'config': conf}
    return render(request, 'header.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import PricingRule
from .forms import PricingRuleForm

@login_required
def pricing_rule_list(request):
    rules = PricingRule.objects.filter(proprietaire=request.user)
    return render(request, 'pricing_rule_list.html', {'rules': rules})

@login_required
def pricing_rule_create(request):
    if request.method == 'POST':
        form = PricingRuleForm(request.POST)
        if form.is_valid():
            rule = form.save(commit=False)
            rule.proprietaire = request.user
            rule.save()
            return redirect('pricing_rule_list') 
    else:
        form = PricingRuleForm()
    return render(request, 'pricing_rule_form.html', {'form': form})

@login_required
def pricing_rule_update(request, pk):
    rule = get_object_or_404(PricingRule, pk=pk)
    if request.method == 'POST':
        form = PricingRuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('pricing_rule_list')
    else:
        form = PricingRuleForm(instance=rule)
    return render(request, 'pricing_rule_form.html', {'form': form})

@login_required
def pricing_rule_delete(request, pk):
    rule = get_object_or_404(PricingRule, pk=pk)
    if request.method == 'POST':
        rule.delete()
        return redirect('pricing_rule_list')
    return render(request, 'pricing_rule_confirm_delete.html', {'rule': rule})
