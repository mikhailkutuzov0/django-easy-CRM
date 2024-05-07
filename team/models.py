from django.contrib.auth.models import User

from django.db import models


class Team(models.Model):
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

    def __str__(self):
        return self.name
