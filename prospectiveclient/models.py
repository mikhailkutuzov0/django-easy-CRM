from django.contrib.auth.models import User
from django.db import models

from team.models import Team


class ProspectiveClient(models.Model):
    """
    Модель заполнения потенциальных клиентов, с назначением статуса
    клиенту и отметками о дате создания/изменения с указанием менеджера.

    Args:
        team (ForeignKey): Состоит в команде
        name (CharField): Имя клиента.
        email (EmailField): Электронная почта клиента.
        description (TextField): Описание клиента.
        status (CharField): Статус клиента.
        priority (CharField): Приоритет клиента.
        created_by (ForeignKey): Менеджер, создавший запись.
        created_at (DateTimeField): Время создания записи.
        modified_at (DateTimeField): Время последнего изменения записи.
    """
    LOW = 'Низкий приоритет'
    MEDIUM = 'Средний приоритет'
    HIGH = 'Высокий приоритет'

    CHOICES_PRIORITY = (
        (LOW, 'Низкий приоритет'),
        (MEDIUM, 'Средний приоритет'),
        (HIGH, 'Высокий приоритет'),
    )

    NEW = 'Новый клиент'
    CONTACTED = 'Уже связались'
    WON = 'В работе'
    LOST = 'Упущен'

    CHOICES_STATUS = (
        (NEW, 'Новый клиент'),
        (CONTACTED, 'Уже связались'),
        (WON, 'В работе'),
        (LOST, 'Упущен'),
    )

    team = models.ForeignKey(
        Team,
        related_name='prospectiveclients',
        on_delete=models.CASCADE,
        verbose_name='Состоит в команде'
    )
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    description = models.TextField(
        blank=True, null=True, verbose_name='Описание')
    status = models.CharField(
        max_length=45,
        choices=CHOICES_STATUS,
        default=NEW,
        verbose_name='Статус'
    )
    priority = models.CharField(
        max_length=45,
        choices=CHOICES_PRIORITY,
        default=MEDIUM,
        verbose_name='Приоритет'
    )
    converted_to_client = models.BooleanField(
        default=False, verbose_name='Стал клиентом')
    created_by = models.ForeignKey(
        User,
        related_name='clients',
        on_delete=models.CASCADE,
        verbose_name='Создано кем'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано в')
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='Изменено в')

    class Meta():
        db_table = 'prospective_client'
        ordering = ('name',)
        verbose_name = 'Потенциальный клиент'
        verbose_name_plural = 'Потенциальные клиенты'

    def __str__(self):
        return f'{self.name} | {self.status} | {self.priority}'


class Comment(models.Model):
    team = models.ForeignKey(
        Team,
        related_name='prospectiveclients_comments',
        on_delete=models.CASCADE,
        verbose_name='Команда потенциального клиента'
    )
    prospectiveclient = models.ForeignKey(
        ProspectiveClient,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Для кого оставлен комментарий'
    )
    content = models.TextField(
        blank=True, null=True, verbose_name='Содержание')
    created_by = models.ForeignKey(
        User,
        related_name='prospectiveclients_comments',
        on_delete=models.CASCADE,
        verbose_name='Создано кем'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано в')

    class Meta():
        db_table = 'prospective_client_comment'
        verbose_name = 'Коментарий для потенциального клиента'
        verbose_name_plural = 'Коментарии для потенциальных клиентов'

    def __str__(self):
        return f'{self.created_by} - {self.content}'
