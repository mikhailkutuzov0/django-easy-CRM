from django.urls import path
from . import views

app_name = 'prospectiveclient'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_prospective_client, name='all'),
    path('<int:pk>/', views.prospective_client_detail, name='detail'),
    path('<int:pk>/delete/', views.delete_prospective_client, name='delete'),
    path('<int:pk>/edit/', views.edit_prospective_client, name='edit'),
    path('<int:pk>/convert/', views.convert_to_client, name='convert'),
    path('add/', views.add_prospective_client, name='add'),
]
