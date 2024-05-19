from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from prospectiveclient.models import ProspectiveClient
from client.models import Client


@login_required
def dashboard(request):
    """
    Отображает панель управления с последними добавленными клиентами.

    Args:
        request (HttpRequest): Запрос, с информацей текущем пользователе.

    Returns:
        HttpResponse: Ответ, содержащий HTML шаблон панели управления.
    """
    team = request.user.userprofile.get_active_team()
    prospective_clients = ProspectiveClient.objects.filter(
        team=team, converted_to_client=False).order_by('-created_at')[0:5]
    clients = Client.objects.filter(
        team=team).order_by('-created_at')[0:5]

    return render(request, 'dashboard/dashboard.html', {
        'prospective_clients': prospective_clients,
        'clients': clients,
    })
