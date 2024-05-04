from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('/user/login/')
    else:
        form = UserCreationForm(request.POST)

    return render(request, 'userprofile/registration.html', {'form': form})
