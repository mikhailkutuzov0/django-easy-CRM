from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import AddProspectiveClient
from .models import ProspectiveClient


@login_required
def all_prospective_client(request):
    all_clients = ProspectiveClient.objects.filter(created_by=request.user)
    return render(request,
                  'prospectiveclient/all.html', {'all_clients': all_clients}
                  )


@login_required
def add_prospective_client(request):
    if request.method == 'POST':
        form = AddProspectiveClient(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()

            return redirect('/dashboard/')
    else:
        form = AddProspectiveClient()
    return render(request, 'prospectiveclient/add.html', {'form': form})
