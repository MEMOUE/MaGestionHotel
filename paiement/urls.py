from django.urls import path
from paiement.views import home_paiement
from . import views 

urlpatterns = [
    path("", home_paiement, name="home_paiement"),
    path('autres-revenus-couts/', views.autre_revenu_cout_list, name='autre_revenu_cout_list'),
    path('autres-revenus-couts/new/', views.autre_revenu_cout_create, name='autre_revenu_cout_create'),
    path('autres-revenus-couts/<int:pk>/edit/', views.autre_revenu_cout_update, name='autre_revenu_cout_update'),
    path('autres-revenus-couts/<int:pk>/delete/', views.autre_revenu_cout_delete, name='autre_revenu_cout_delete'),
]

   
