from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team.models import Team
from .forms import AddProspectiveClient
from .models import ProspectiveClient
from client.models import Client


@login_required
def all_prospective_client(request):
    all_clients = ProspectiveClient.objects.filter(
        created_by=request.user, converted_to_client=False)
    return render(request,
                  'prospectiveclient/all.html', {'all_clients': all_clients}
                  )


@login_required
def prospective_client_detail(request, pk):
    client = get_object_or_404(
        ProspectiveClient, created_by=request.user, pk=pk)

    return render(
        request, 'prospectiveclient/client_detail.html', {'client': client}
    )


@login_required
def delete_prospective_client(request, pk):
    client = get_object_or_404(
        ProspectiveClient, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, 'Потенциальный клиент был удален!')
    return redirect('/dashboard/prospective-clients/')


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
            return redirect('/dashboard/prospective-clients/')
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

            return redirect('/dashboard/prospective-clients/')
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
    return redirect('/dashboard/prospective-clients/')
