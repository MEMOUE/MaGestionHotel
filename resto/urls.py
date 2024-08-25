from django.urls import path
from resto.views import CreateMenu, ListMenu, UpdateMenu, DeleteMenu, gestion_commande, modifier_commande, supprimer_commande


urlpatterns = [
    path("home-resto", ListMenu.as_view(), name="home-resto"),
    path("add-menu/", CreateMenu.as_view(), name="add-menu"),
    path("update-menu/<int:id>", UpdateMenu.as_view(), name="update-menu"),
    path("delete-menu/<int:id>", DeleteMenu.as_view(), name="delete-menu"),
    path('reservation/<int:reservation_id>/commandes/',gestion_commande, name='gestion_commande'),
    path('commande/<int:commande_id>/modifier/',modifier_commande, name='modifier_commande'),
    path('commande/<int:commande_id>/supprimer/',supprimer_commande, name='supprimer_commande'),

]