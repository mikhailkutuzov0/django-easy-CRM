from django.urls import path

from . import views

app_name = 'team'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.all_teams, name='all'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/edit/', views.edit_team, name='edit'),
    path('<int:pk>/activate/', views.teams_activate, name='activate'),
]
