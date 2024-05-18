from django import forms
from .models import ProspectiveClient, Comment


class AddProspectiveClient(forms.ModelForm):
    class Meta:
        model = ProspectiveClient
        fields = ('name', 'email', 'description', 'priority', 'status',)


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
