from django.urls import path

from . import views

app_name = 'client'  # Пространство имен для URL-адресов

urlpatterns = [
    # URL для отображения всех клиентов
    path('', views.all_clients, name='all'),
    # URL для отображения деталей клиента
    path('<int:pk>/', views.client_detail, name='detail'),
    # URL для удаления клиента
    path('<int:pk>/delete/', views.delete_client, name='delete'),
    # URL для редактирования клиента
    path('<int:pk>/edit/', views.edit_client, name='edit'),
    # URL для добавления комментария
    path('<int:pk>/add-comment/', views.client_detail, name='add_comment'),
    # URL для добавления файла
    path('<int:pk>/add-file/', views.client_add_file, name='add_file'),
    # URL для добавления нового клиента
    path('add/', views.add_client, name='add'),
    # URL для экспорта списка клиентов в CSV
    path('export/', views.client_export, name='export'),
]
