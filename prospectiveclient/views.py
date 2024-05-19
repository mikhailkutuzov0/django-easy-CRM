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
    model = ProspectiveClient

    def get_queryset(self):
        queryset = super(ProspectiveClientListView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, converted_to_client=False)


class ProspectiveClientDetailView(LoginRequiredMixin, DetailView):
    model = ProspectiveClient

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(ProspectiveClientDetailView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))


class ProspectiveClientDeleteView(LoginRequiredMixin, DeleteView):
    model = ProspectiveClient

    success_url = reverse_lazy('prospectiveclient:all')

    def get_queryset(self):
        queryset = super(ProspectiveClientDeleteView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProspectiveClientCreateView(LoginRequiredMixin, CreateView):
    model = ProspectiveClient
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('prospectiveclient:all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.get_active_team()
        context['team'] = team
        context['title'] = 'Добавить потенциального клиента'

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.get_active_team()
        self.object.save()

        return redirect(self.success_url)


class ProspectiveClientUpdateView(LoginRequiredMixin, UpdateView):
    model = ProspectiveClient
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('prospectiveclient:all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить потенциального клиента'

        return context

    def get_queryset(self):
        queryset = super(ProspectiveClientUpdateView, self).get_queryset()
        team = self.request.user.userprofile.active_team

        return queryset.filter(team=team, pk=self.kwargs.get('pk'))


class AddFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
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
    def post(self, request, *args, **kwargs):
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
    def get(self, request, *args, **kwargs):
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
