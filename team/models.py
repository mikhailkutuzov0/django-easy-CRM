from django.contrib.auth.models import User

from django.db import models


class ClientTeamAccess(models.Model):
    """
    Модель ClientTeamAccess представляет доступ командам к клиентам в
    системе. Дает возможность ограничить максимальное количество клиентов.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    max_prospective_clients = models.IntegerField()
    max_clients = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'client_team_access'
        verbose_name = 'Доступ к клиенту'
        verbose_name_plural = 'Доступ к клиентам'


class Team(models.Model):
    client_team_access = models.ForeignKey(
        ClientTeamAccess,
        related_name='teams',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Доступ к клиентам')
    name = models.CharField(max_length=100, verbose_name='Название')
    members = models.ManyToManyField(
        User, related_name='teams', verbose_name='Участники')
    created_by = models.ForeignKey(
        User,
        related_name='created_teams',
        on_delete=models.CASCADE,
        verbose_name='Кем создана'
    )
    created_at = models.DateTimeField(
        auto_now=True, verbose_name='Когда создана')

    class Meta():
        db_table = 'team'
        verbose_name = 'Команда'
        verbose_name_plural: str = 'Команды'

    def get_client_team_access(self):
        if self.client_team_access:
            return self.client_team_access
        else:
            if ClientTeamAccess.objects.count() > 0:
                self.client_team_access = ClientTeamAccess.objects.all().first()
                self.save()
            else:
                client_team_access = ClientTeamAccess.objects.create(
                    name='First', max_leads=5, max_clients=5)
                self.client_team_access = client_team_access
                self.save()

            return self.client_team_access

    def __str__(self):
        return self.name
