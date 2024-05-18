from django import forms
from .models import Client, ClientFile, Comment


class AddClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description')


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)


class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)
