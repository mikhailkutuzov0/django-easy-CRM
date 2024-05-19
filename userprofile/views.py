from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from team.models import Team
from userprofile.forms import SignupForm

from .models import UserProfile


def registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            team = Team.objects.create(
                name='Team name', created_by=user)
            team.members.add(user)
            team.save()

            UserProfile.objects.create(user=user, active_team=team)

            return redirect('/user/login/')
    else:
        form = SignupForm(request.POST)

    return render(request, 'userprofile/registration.html', {'form': form})


@login_required
def my_account(request):
    team = Team.objects.filter(created_by=request.user)[0]
    return render(request, 'userprofile/myaccount.html', {'team': team})
