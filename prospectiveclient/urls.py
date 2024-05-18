from django.urls import path
from . import views

app_name = 'prospectiveclient'  # Пространство имен для URL-адресов

urlpatterns = [
    path('', views.ProspectiveClientListView.as_view(), name='all'),
    path(
        '<int:pk>/',
        views.ProspectiveClientDetailView.as_view(),
        name='detail'
    ),
    path(
        '<int:pk>/delete/',
        views.ProspectiveClientDeleteView.as_view(),
        name='delete'
    ),
    path(
        '<int:pk>/edit/',
        views.ProspectiveClientUpdateView.as_view(),
        name='edit'
    ),
    path(
        '<int:pk>/convert/',
        views.ConvertToClientView.as_view(),
        name='convert'
    ),
    path(
        '<int:pk>/add-comment/',
        views.AddCommentView.as_view(),
        name='add_comment'
    ),
    path('add/', views.ProspectiveClientCreateView.as_view(), name='add'),
]
