from django.urls import path

from . import views

app_name = 'client'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_clients, name='all'),
    path('<int:pk>/', views.client_detail, name='detail'),
    path('<int:pk>/delete/', views.delete_client, name='delete'),
    path('<int:pk>/edit/', views.edit_client, name='edit'),
    path('<int:pk>/add-comment/', views.client_detail, name='add_comment'),
    path('add/', views.add_client, name='add'),
]
