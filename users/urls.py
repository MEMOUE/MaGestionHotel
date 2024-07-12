from django.contrib.auth import views
from django.urls import path
from .views import inscription, connexion, deconnexion, home, menusysteme, list_secondary_users, create_secondary_user, update_secondary_user,delete_secondary_user, secondary_user_login, verify_email


urlpatterns = [
    path("inscription/", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("home/", home, name="home-users"),
    path("menusysteme/",menusysteme, name="menusysteme"),
    path("deconnexion", deconnexion, name="deconnexion"),

    # gestion de reinitialisation de email
    path('password_reset/', views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),

    #change password
    path('password_change/', views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),

    path('create_secondary_user/', create_secondary_user, name='create_secondary_user'),
    path('update_secondary_user/<int:user_id>/', update_secondary_user, name='update_secondary_user'),
    path('delete_secondary_user/<int:user_id>/', delete_secondary_user, name='delete_secondary_user'),
    path('list_secondary_user/', list_secondary_users, name='list_secondary_users'),
    path('secondary_user_login/', secondary_user_login, name='secondary_user_login'),

    #verification email à l'inscrption 
    path('verify-email/<str:token>/', verify_email, name='verify_email'),
    
]
