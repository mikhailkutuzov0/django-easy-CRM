from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from team.models import Team

from .models import UserProfile


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            team = Team.objects.create(
                name='Team name', created_by=request.user)
            team.members.add(request.user)
            team.save()
            return redirect('/user/login/')
    else:
        form = UserCreationForm(request.POST)

    return render(request, 'userprofile/registration.html', {'form': form})


@login_required
def my_account(request):
    team = Team.objects.filter(created_by=request.user)[0]
    return render(request, 'userprofile/myaccount.html', {'team': team})
