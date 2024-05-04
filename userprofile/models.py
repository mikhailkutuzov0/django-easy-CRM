from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, related_name='userprofiles', on_delete=models.CASCADE)

    class Meta():
        db_table = 'userprofile'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
