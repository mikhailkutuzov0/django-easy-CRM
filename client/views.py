from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Client


@login_required
def all_clients(request):
    clients = Client.objects.filter(created_by=request.user)

    return render(request, 'client/all.html', {'clients': clients})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    return render(request, 'client/client_detail.html', {'client': client})
