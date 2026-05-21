from django.urls import path
from . import views

urlpatterns = [
    path('stock-in/', views.stockin_list, name='stockin_list'),
    path('stock-in/add/', views.stockin_create, name='stockin_create'),
    path('stock-out/', views.stockout_list, name='stockout_list'),
    path('stock-out/add/', views.stockout_create, name='stockout_create'),
]