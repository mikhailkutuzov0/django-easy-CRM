from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from team.models import Team
from .forms import TeamForm


@login_required
def all_teams(request):
    """
    Отображает список всех команд пользователя.

    Args:
        request (HttpRequest): Запрос, с информацией о текущем пользователе.

    Returns:
        HttpResponse: Ответ, содержащий HTML шаблон со списком команд.
    """
    teams = Team.objects.filter(members__in=[request.user])

    return render(request, 'team/all_teams.html', {'teams': teams})


@login_required
def detail(request, pk):
    """
    Отображает детали команды.

    Args:
        request (HttpRequest): Запрос, с информацией о текущем пользователе.
        pk (int): Первичный ключ команды.

    Returns:
        HttpResponse: Ответ, содержащий HTML шаблон с деталями команды.
    """
    team = get_object_or_404(Team, members__in=[request.user], pk=pk)

    return render(request, 'team/detail.html', {'team': team})


@login_required
def teams_activate(request, pk):
    team = Team.objects.filter(members__in=[request.user]).get(pk=pk)
    userprofile = request.user.userprofile
    userprofile.active_team = team
    userprofile.save()

    return redirect('team:detail', pk=pk)


@login_required
def edit_team(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, 'Изменения сохранены')
            return redirect('userprofile:my-account')
    else:
        form = TeamForm(instance=team)
    return render(request, 'team/edit_team.html', {'team': team, 'form': form})
