from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')
    created_by = models.ForeignKey(
        User,
        related_name='prospectiveclients',
        on_delete=models.CASCADE,
        verbose_name='Создано кем'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано в ')
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='Изменено в')

    class Meta():
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name
