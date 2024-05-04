from django.urls import path
from . import views

app_name = 'dashboard'  # Пространство имен для URL-адресов

urlpatterns = [
    # Главная страница:
    path('', views.dashboard, name='dashboard'),
]
