from django.urls import path
from . import views

app_name = 'dashboard'  # Пространство имен для URL-адресов

urlpatterns = [
    # URL для отображения панели :
    path('', views.dashboard, name='index'),
]
