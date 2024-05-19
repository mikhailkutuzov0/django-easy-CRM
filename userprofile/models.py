from django.contrib.auth.models import User
from django.db import models

from team.models import Team


class UserProfile(models.Model):
    """
    Модель для представления профиля пользователя.

    Attributes:
        user (OneToOneField): Пользователь, связанный с профилем.
        active_team (ForeignKey): Активная команда пользователя.
    """
    user = models.OneToOneField(
        User, related_name='userprofile', on_delete=models.CASCADE)
    active_team = models.ForeignKey(
        Team,
        related_name='userprofiles',
        blank=True, null=True,
        on_delete=models.CASCADE
    )

    def get_active_team(self):
        """
        Возвращает активную команду пользователя.

        Returns:
            Team: Активная команда пользователя.
        """
        if self.active_team:
            return self.active_team
        else:
            return Team.objects.filter(members__in=[self.user.id]).first()

    class Meta():
        db_table = 'userprofile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
