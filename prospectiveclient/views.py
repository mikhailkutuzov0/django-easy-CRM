from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from team.models import Team
from .forms import AddProspectiveClient
from .models import ProspectiveClient
from client.models import Client


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

    def get_queryset(self):
        queryset = super(ProspectiveClientDetailView, self).get_queryset()

        return queryset.filter(
            created_by=self.request.user, pk=self.kwargs.get('pk')
        )


@login_required
def delete_prospective_client(request, pk):
    client = get_object_or_404(
        ProspectiveClient, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, 'Потенциальный клиент был удален!')
    return redirect('prospectiveclient:all')


@login_required
def add_prospective_client(request):
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddProspectiveClient(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, 'Потенциальный клиент был создан!')
            return redirect('prospectiveclient:all')
    else:
        form = AddProspectiveClient()
    return render(request, 'prospectiveclient/add.html', {
        'form': form,
        'team': team,
    })


@login_required
def edit_prospective_client(request, pk):
    client = get_object_or_404(
        ProspectiveClient, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = AddProspectiveClient(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(
                request, 'Клиент был отредактирован!')

            return redirect('prospectiveclient:all')
    else:
        form = AddProspectiveClient(instance=client)

    return render(request, 'prospectiveclient/edit_client.html', {
        'form': form
    })


@login_required
def convert_to_client(request, pk):
    client_to_convert = get_object_or_404(
        ProspectiveClient, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]
    Client.objects.create(
        name=client_to_convert.name,
        email=client_to_convert.email,
        team=team,
        description=client_to_convert.description,
        created_by=request.user
    )
    client_to_convert.converted_to_client = True
    client_to_convert.save()
    messages.success(request, f'{client_to_convert.name} теперь клиент!')
    return redirect('prospectiveclient:all')
