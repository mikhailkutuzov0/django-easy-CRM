from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team.models import Team
from .models import Client
from .forms import AddClient


@login_required
def all_clients(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/all.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})


@login_required
def add_client(request):
    if request.method == 'POST':
        form = AddClient(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, 'Клиент был создан!')
            return redirect('/dashboard/clients/')
    else:
        form = AddClient()
    return render(request, 'client/add.html', {'form': form})


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, 'Клиент был удален!')
    return redirect('/dashboard/clients/')


@login_required
def edit_client(request, pk):
    client = get_object_or_404(
        Client, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = AddClient(request.POST, instance=client)

        if form.is_valid():
            form.save()

            messages.success(
                request, 'Клиент был отредактирован!')

            return redirect('/dashboard/clients/')
    else:
        form = AddClient(instance=client)

    return render(request, 'client/edit_client.html', {
        'form': form
    })
