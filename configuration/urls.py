from django.urls import path

from configuration.views import home_config, CreateConfig, DetailConfig, ListConfig, update_config, \
    UpdateConfig, header, delete_config
from . import views



urlpatterns = [
    path("", home_config, name="home-config"),
    path("create/", CreateConfig.as_view(), name="create-config"),
    path("list/", ListConfig.as_view(), name="list-config"),
    path("detail/<int:pk>", DetailConfig.as_view(), name="detail-config"),
    path("update/<int:pk>", UpdateConfig.as_view(), name="update-config"),
    path("delete/<int:pk>/", delete_config, name="delete-config"),
    path("header/", header, name="header"),


    path('rules/', views.pricing_rule_list, name='pricing_rule_list'),
    path('rules/new/', views.pricing_rule_create, name='pricing_rule_create'),
    path('rules/<int:pk>/edit/', views.pricing_rule_update, name='pricing_rule_update'),
    path('rules/<int:pk>/delete/', views.pricing_rule_delete, name='pricing_rule_delete'),
]