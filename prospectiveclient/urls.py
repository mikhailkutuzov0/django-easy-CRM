from django.urls import path
from . import views

app_name = 'prospectiveclient'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_prospective_client, name='all'),
    path('add/', views.add_prospective_client, name='add-new'),
]
