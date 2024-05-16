from django.urls import path
from . import views

app_name = 'main'  # Пространство имен для URL-адресов

urlpatterns = [
    # Главная страница:
    path('', views.index, name='index'),
    # Страница о нас
    path('about/', views.about, name='about'),

]
