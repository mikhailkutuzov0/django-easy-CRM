from django.contrib import admin
from .models import ProspectiveClient, Comment, ProspectiveClientFile


admin.site.register(ProspectiveClient)
admin.site.register(Comment)
admin.site.register(ProspectiveClientFile)
