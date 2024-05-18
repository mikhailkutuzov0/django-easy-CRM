import csv
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team.models import Team
from .models import Client
from .forms import AddClient, AddCommentForm, AddFileForm


@login_required
def client_export(request):
    clients = Client.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="clients.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['Client', 'Description', 'Created at', 'Created by'])

    for client in clients:
        writer.writerow([client.name, client.description,
                        client.created_at, client.created_by])

    return response


@login_required
def all_clients(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/all.html', {'clients': clients})


@login_required
def client_add_file(request, pk):
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            file = form.save(commit=False)
            file.team = team
            file.client_id = pk
            file.created_by = request.user
            file.save()

            return redirect('client:detail', pk=pk)
    return redirect('client:detail', pk=pk)


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    team = Team.objects.filter(created_by=request.user)[0]

    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('client:detail', pk=pk)
    else:
        form = AddCommentForm()

    return render(
        request,
        'client/client_detail.html',
        {
            'client': client,
            'form': form,
            'fileform': AddFileForm(),
        }
    )


@login_required
def add_client(request):
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddClient(request.POST)

        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            messages.success(request, 'Клиент был создан!')
            return redirect('client:all')
    else:
        form = AddClient()
    return render(request, 'client/add.html', {
        'form': form,
        'team': team,
    })


@login_required
def delete_client(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    messages.success(request, 'Клиент был удален!')
    return redirect('client:all')


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

            return redirect('client:all')
    else:
        form = AddClient(instance=client)

    return render(request, 'client/edit_client.html', {
        'form': form
    })
