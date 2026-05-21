from django.urls import path
from . import views

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('add/', views.supplier_create, name='supplier_create'),
    path('delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
]