from django import forms
from .models import ProspectiveClient


class AddProspectiveClient(forms.ModelForm):
    class Meta:
        model = ProspectiveClient
        fields = ('name', 'email', 'description', 'priority', 'status',)
