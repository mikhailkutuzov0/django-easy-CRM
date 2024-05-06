from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AddProspectiveClient
from .models import ProspectiveClient


@login_required
def all_prospective_client(request):
    all_clients = ProspectiveClient.objects.filter(created_by=request.user)
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
    if request.method == 'POST':
        form = AddProspectiveClient(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            return redirect('/dashboard/prospective-clients/')
    else:
        form = AddProspectiveClient()
    return render(request, 'prospectiveclient/add.html', {'form': form})
