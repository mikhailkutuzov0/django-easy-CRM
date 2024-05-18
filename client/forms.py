from django import forms
from .models import Client, Comment


class AddClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description')


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
