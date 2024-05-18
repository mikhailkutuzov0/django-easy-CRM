from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    ListView, DetailView, DeleteView, UpdateView, CreateView
)

from .forms import AddCommentForm, AddFileForm
from team.models import Team
from .models import ProspectiveClient
from client.models import Client, Comment as ClientComment


class ProspectiveClientListView(ListView):
    model = ProspectiveClient

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(ProspectiveClientListView, self).get_queryset()

        return queryset.filter(
            created_by=self.request.user, converted_to_client=False
        )


class ProspectiveClientDetailView(DetailView):
    model = ProspectiveClient

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(ProspectiveClientDetailView, self).get_queryset()

        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk')
        )


class ProspectiveClientDeleteView(DeleteView):
    model = ProspectiveClient

    success_url = reverse_lazy('prospectiveclient:all')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(ProspectiveClientDeleteView, self).get_queryset()

        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk')
        )

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProspectiveClientCreateView(CreateView):
    model = ProspectiveClient
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('prospectiveclient:all')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.filter(created_by=self.request.user)[0]
        context['team'] = team
        context['title'] = 'Добавить потенциального клиента'

        return context

    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = team
        self.object.save()

        return redirect(self.success_url)


class ProspectiveClientUpdateView(UpdateView):
    model = ProspectiveClient
    fields = ('name', 'email', 'description', 'priority', 'status',)
    success_url = reverse_lazy('prospectiveclient:all')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить потенциального клиента'

        return context

    def get_queryset(self):
        queryset = super(ProspectiveClientUpdateView, self).get_queryset()

        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk')
        )


class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            file = form.save(commit=False)
            file.team = team
            file.prospectiveclient_id = pk
            file.created_by = request.user
            file.save()

        return redirect('prospectiveclient:detail', pk=pk)


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form = AddCommentForm(request.POST)
        if form.is_valid():
            team = Team.objects.filter(created_by=self.request.user)[0]
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.prospectiveclient_id = pk
            comment.save()
        return redirect('prospectiveclient:detail', pk=pk)


class ConvertToClientView(View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        client_to_convert = get_object_or_404(
            ProspectiveClient, created_by=request.user, pk=pk
        )
        team = Team.objects.filter(created_by=request.user)[0]
        client = Client.objects.create(
            name=client_to_convert.name,
            email=client_to_convert.email,
            team=team,
            description=client_to_convert.description,
            created_by=request.user
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
