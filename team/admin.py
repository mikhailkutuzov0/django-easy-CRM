from django.contrib import admin

from .models import Team, ClientTeamAccess

admin.site.register(Team)
admin.site.register(ClientTeamAccess)
