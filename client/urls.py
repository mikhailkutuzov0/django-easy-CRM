from django.urls import path

from . import views

app_name = 'client'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_clients, name='all'),
    path('<int:pk>/', views.client_detail, name='client-detail'),
    path('<int:pk>/delete/', views.delete_client, name='client-delete'),
    path('<int:pk>/edit/', views.edit_client, name='client-edit'),
    path('add/', views.add_client, name='client-add'),

]
