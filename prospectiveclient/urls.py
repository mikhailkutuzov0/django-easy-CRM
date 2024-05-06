from django.urls import path
from . import views

app_name = 'prospectiveclient'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_prospective_client, name='all'),
    path('<int:pk>/', views.prospective_client_detail, name='client-detail'),
    path('add/', views.add_prospective_client, name='add-new'),
]
