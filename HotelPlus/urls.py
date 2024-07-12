from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import index, pdf, Facture
from django.conf import settings
from users import views as user_views
from django.conf.urls import handler400, handler403, handler404, handler500




urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("users/", include("users.urls")),
    path("chambre/", include("chambre.urls")),
    path("reservation/", include("reservation.urls")),
    path("resto/", include("resto.urls")),
    path("paiement/", include("paiement.urls")),
    path("config/", include("configuration.urls")),
    path("stats/", include("statistique.urls")),
    # authentification google
    path('accounts/', include('allauth.urls')),
    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    
# Définir les gestionnaires d'erreurs personnalisés
handler404 = 'users.views.custom_page_not_found_view'
handler500 = 'users.views.custom_error_view'
handler403 = 'users.views.custom_permission_denied_view'
handler400 = 'users.views.custom_bad_request_view'