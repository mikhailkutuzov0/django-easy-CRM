from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView, DeleteView, UpdateView, CreateView
)

from .forms import AddCommentForm, AddFileForm
from .models import ProspectiveClient
from client.models import Client, Comment as ClientComment


class ProspectiveClientListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка потенциальных клиентов.

    Attributes:
        model (Model): Модель, используемая для представления.
    """
    model = ProspectiveClient

    def get_queryset(self):
        """
        Возвращает queryset для текущей команды пользователя.

        Returns:
            QuerySet: Запрос с отфильтрованными потенциальными клиентами.
        """
        queryset = super(ProspectiveClientListView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, converted_to_client=False)


class ProspectiveClientDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения деталей потенциального клиента.

    Attributes:
        model (Model): Модель, используемая для представления.
    """
    model = ProspectiveClient

    def get_context_data(self, **kwargs):
        """
        Возвращает контекстные данные для шаблона.

        Returns:
            dict: Контекстные данные.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        """
        Возвращает queryset для текущей команды пользователя.

        Returns:
            QuerySet: Запрос с отфильтрованным потенциальным клиентом.
        """
        queryset = super(ProspectiveClientDetailView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))


class ProspectiveClientDeleteView(LoginRequiredMixin, DeleteView):
    """
    Представление для удаления потенциального клиента.

    Attributes:
        model (Model): Модель, используемая для представления.
        success_url (str): URL для перенаправления после успешного удаления.
    """
    model = ProspectiveClient

    success_url = reverse_lazy('prospectiveclient:all')

    def get_queryset(self):
        """
        Возвращает queryset для текущей команды пользователя.

        Returns:
            QuerySet: Запрос с отфильтрованным потенциальным клиентом.
        """
        queryset = super(ProspectiveClientDeleteView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET запрос.

        Args:
            request (HttpRequest): Запрос, с информацией о текущем пользователе

        Returns:
            HttpResponse: Перенаправление на success_url.
        """
        return self.post(request, *args, **kwargs)


class ProspectiveClientCreateView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового потенциального клиента.

    Attributes:
        model (Model): Модель, используемая для представления.
        fields (tuple): Поля формы.
        success_url (str): URL для перенаправления после успешного создания.
    """
    model = ProspectiveClient
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('prospectiveclient:all')

    def get_context_data(self, **kwargs):
        """
        Возвращает контекстные данные для шаблона.

        Returns:
            dict: Контекстные данные.
        """
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.get_active_team()
        context['team'] = team
        context['title'] = 'Добавить потенциального клиента'

        return context

    def form_valid(self, form):
        """
        Проверяет форму на валидность и сохраняет объект.

        Args:
            form (ModelForm): Форма для проверки и сохранения.

        Returns:
            HttpResponse: Перенаправление на success_url.
        """
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.get_active_team()
        self.object.save()

        return redirect(self.success_url)


class ProspectiveClientUpdateView(LoginRequiredMixin, UpdateView):
    """
    Представление для обновления данных потенциального клиента.

    Attributes:
        model (Model): Модель, используемая для представления.
        fields (tuple): Поля формы.
        success_url (str): URL для перенаправления после успешного обновления.
    """
    model = ProspectiveClient
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('prospectiveclient:all')

    def get_context_data(self, **kwargs):
        """
        Возвращает контекстные данные для шаблона.

        Returns:
            dict: Контекстные данные.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить потенциального клиента'

        return context

    def get_queryset(self):
        """
        Возвращает queryset для текущей команды пользователя.

        Returns:
            QuerySet: Запрос с отфильтрованным потенциальным клиентом.
        """
        queryset = super(ProspectiveClientUpdateView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))


class AddFileView(LoginRequiredMixin, View):
    """
    Представление для добавления файла к потенциальному клиенту.

    Methods:
        post: Обрабатывает POST запрос для добавления файла.
    """

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос для добавления файла.

        Args:
            request (HttpRequest): Запрос, с информацией о текущем пользователе

        Returns:
            HttpResponse: Перенаправление на детали потенциального клиента.
        """
        pk = kwargs.get('pk')
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = self.request.user.userprofile.get_active_team()
            file.prospectiveclient_id = pk
            file.created_by = request.user
            file.save()

        return redirect('prospectiveclient:detail', pk=pk)


class AddCommentView(LoginRequiredMixin, View):
    """
    Представление для добавления комментария к потенциальному клиенту.

    Methods:
        post: Обрабатывает POST запрос для добавления комментария.
    """

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает POST запрос для добавления комментария.

        Args:
            request (HttpRequest): Запрос, с информацией о текущем пользователе

        Returns:
            HttpResponse: Перенаправление на детали потенциального клиента.
        """
        pk = kwargs.get('pk')
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.get_active_team()
            comment.created_by = request.user
            comment.prospectiveclient_id = pk
            comment.save()
        return redirect('prospectiveclient:detail', pk=pk)


class ConvertToClientView(LoginRequiredMixin, View):
    """
    Представление для конвертации потенциального клиента в клиента.

    Methods:
        get: Обрабатывает GET запрос для конвертации клиента.
    """

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET запрос для конвертации клиента.

        Args:
            request (HttpRequest): Запрос, с информацией о текущем пользователе

        Returns:
            HttpResponse: Редирект на страницу всех потенциальных клиентов.
        """
        pk = self.kwargs.get('pk')
        team = self.request.user.userprofile.active_team
        client_to_convert = get_object_or_404(
            ProspectiveClient, team=team, pk=pk)

        client = Client.objects.create(
            name=client_to_convert.name,
            email=client_to_convert.email,
            description=client_to_convert.description,
            created_by=request.user,
            team=team,
        )
        client_to_convert.converted_to_client = True
        client_to_convert.save()

        comments = client_to_convert.comments.all()

        for comment in comments:
            ClientComment.objects.create(
                client=client,
                content=comment.content,
                created_by=comment.created_by,
                team=team,
            )

        messages.success(request, f'{client_to_convert.name} теперь клиент!')

        return redirect('prospectiveclient:all')
