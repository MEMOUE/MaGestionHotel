from django.urls import path

from configuration.views import home_config, CreateConfig, DetailConfig, ListConfig, regle_prix, ListRegle, update_config, \
    UpdateConfig, update_rule, delete_rule,header,pricing_rule_list
from . import views

app_name = "confighotel"
urlpatterns = [
    path("", home_config, name="home-config"),
    path("create-rule/", regle_prix, name="create-rule"),
    path("list-rule/", ListRegle.as_view(), name="list-rule"),
    path("update-rule/<int:id>", update_rule, name="update-rule"),
    path("delete-rule/<int:id>", delete_rule, name="delete-rule"),
    path("create/", CreateConfig.as_view(), name="create-config"),
    path("list/", ListConfig.as_view(), name="list-config"),
    path("detail/<int:pk>", DetailConfig.as_view(), name="detail-config"),
    path("update-config/<int:pk>", UpdateConfig.as_view(), name="update-config"),
    path("update-config/", update_config, name="update-config"),
    path("header/", header, name="header"),



    path('rules/', pricing_rule_list, name='pricing_rule_list'),
    path('rules/new/', views.pricing_rule_create, name='pricing_rule_create'),
    path('rules/<int:pk>/edit/', views.pricing_rule_update, name='pricing_rule_update'),
    path('rules/<int:pk>/delete/', views.pricing_rule_delete, name='pricing_rule_delete'),
]