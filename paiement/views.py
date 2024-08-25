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



##################################################          Paiement            ##############################################

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Subscription
from .forms import SubscriptionForm
from django.conf import settings
import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64

@login_required
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('payment', subscription_id=subscription.id)
    else:
        form = SubscriptionForm()
    return render(request, 'subscribe.html', {'form': form})

@login_required
def payment(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    token = get_access_token()
    amount = calculate_amount(subscription.duration)
    url = settings.ORANGE_MONEY_PAYMENT_URL
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'merchant_name': 'Your Merchant Name',
        'order_id': str(subscription.id),
        'amount': str(amount),
        'currency': 'XOF',
        'return_url': 'http://127.0.0.1:8000/return_url',
        'cancel_url': 'http://127.0.0.1:8000/cancel_url',
        'notif_url': 'http://127.0.0.1:8000/notification_url'
    }
    response = requests.post(url, headers=headers, json=data)
    
    print("Payment Request URL:", url)
    print("Payment Request Headers:", headers)
    print("Payment Request Data:", data)
    print("Payment Response Status Code:", response.status_code)
    print("Payment Response Text:", response.text)
    
    if response.status_code == 201:
        return redirect(response.json().get('payment_url'))
    else:
        print("Payment initiation failed")
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        return render(request, 'payment_error.html')


def get_access_token():
    url = settings.ORANGE_MONEY_TOKEN_URL
    client_credentials = f"{settings.ORANGE_MONEY_CLIENT_ID}:{settings.ORANGE_MONEY_CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Failed to obtain access token")
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        raise Exception("Failed to obtain access token")

def calculate_amount(duration):
    if duration == 3:
        return 3000  
    elif duration == 6:
        return 6000  
    elif duration == 9:
        return 9000  
    elif duration == 12:
        return 12000  
    return 0

@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        status = data.get('status')
        if status == 'SUCCESS':
            subscription = Subscription.objects.get(id=order_id)
            subscription.activate()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def payment_return(request):
    return render(request, 'payment_success.html')

@login_required
def payment_cancel(request):
    return render(request, 'payment_cancel.html')


############################################## Fin Paiement ######################
