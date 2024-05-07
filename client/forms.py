from django import forms
from .models import Client


class AddClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description')
