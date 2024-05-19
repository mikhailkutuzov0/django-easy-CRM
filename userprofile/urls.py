from django.urls import path
from django.contrib.auth import views as Views
from . import views
from .forms import LoginForm

app_name = 'userprofile'  # Пространство имен для URL-адресов

urlpatterns = [
    # Страница регистрации:
    path('registration/', views.registration, name='registration'),
    # Страница авторизации:
    path(
        'login/',
        Views.LoginView.as_view(
            template_name='userprofile/login.html',
            authentication_form=LoginForm
        ),
        name='login'
    ),
    # Просмотр профиля
    path('my-account/', views.my_account, name='my-account'),
    # Выход из профиля
    path('logout/',  Views.LogoutView.as_view(), name='logout'),

]
