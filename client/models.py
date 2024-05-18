from django.contrib.auth.models import User
from django.db import models
from team.models import Team


class Client(models.Model):
    team = models.ForeignKey(
        Team,
        related_name='clients',
        on_delete=models.CASCADE,
        verbose_name='Состоит в команде'
    )
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
        ordering = ('name',)
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class Comment(models.Model):
    team = models.ForeignKey(
        Team,
        related_name='lients_comments',
        on_delete=models.CASCADE,
        verbose_name='Команда клиента'
    )
    client = models.ForeignKey(
        Client,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Для кого оставлен комментарий'
    )
    content = models.TextField(
        blank=True, null=True, verbose_name='Содержание')
    created_by = models.ForeignKey(
        User,
        related_name='clients_comments',
        on_delete=models.CASCADE,
        verbose_name='Создано кем'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано в')

    class Meta():
        db_table = 'client_comment'
        verbose_name = 'Коментарий для клиента'
        verbose_name_plural = 'Коментарии для клиентов'

    def __str__(self):
        return f'{self.created_by} - {self.content}'
