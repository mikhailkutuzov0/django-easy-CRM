from django.urls import path

from . import views

app_name = 'client'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_clients, name='all'),
    path('<int:pk>/', views.client_detail, name='client-detail'),
]
