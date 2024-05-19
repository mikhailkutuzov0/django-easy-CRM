from django.urls import path
from . import views

app_name = 'prospectiveclient'  # Пространство имен для URL-адресов

urlpatterns = [
    # URL для отображения всех потенциальных клиентов
    path('', views.ProspectiveClientListView.as_view(), name='all'),
    # URL для отображения деталей потенциального клиента
    path(
        '<int:pk>/',
        views.ProspectiveClientDetailView.as_view(),
        name='detail'
    ),
    # URL для удаления потенциального клиента
    path(
        '<int:pk>/delete/',
        views.ProspectiveClientDeleteView.as_view(),
        name='delete'
    ),
    # URL для редактирования потенциального клиента
    path(
        '<int:pk>/edit/',
        views.ProspectiveClientUpdateView.as_view(),
        name='edit'
    ),
    # URL для конвертации потенциального клиента в клиента
    path(
        '<int:pk>/convert/',
        views.ConvertToClientView.as_view(),
        name='convert'
    ),
    # URL для добавления комментария к потенциальному клиенту
    path(
        '<int:pk>/add-comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    # URL для добавления файла к потенциальному клиенту
    path(
        '<int:pk>/add-file/',
        views.AddFileView.as_view(),
        name='add_file'
    ),
    # URL для добавления нового потенциального клиента
    path('add/', views.ProspectiveClientCreateView.as_view(), name='add'),
]
