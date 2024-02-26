from django.contrib.auth import views
from django.urls import path
from .views import inscription, connexion, deconnexion, home


urlpatterns = [
    path("inscription/", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("home/", home, name="home-users"),
    path("deconnexion", deconnexion, name="deconnexion"),

    # gestion de reinitialisation de email
    path('password_reset/', views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

]
