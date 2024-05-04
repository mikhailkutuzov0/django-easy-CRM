from django.urls import path
from django.contrib.auth import views as Views
from . import views

app_name = 'userprofile'  # Пространство имен для URL-адресов

urlpatterns = [
    # Страница регистрации:
    path('registration/', views.registration, name='registration'),
    # Страница авторизации:
    path(
        'login/',
        Views.LoginView.as_view(template_name='userprofile/login.html'),
        name='login'
    ),
    path('logout/',  Views.LogoutView.as_view(), name='logout'),

]
