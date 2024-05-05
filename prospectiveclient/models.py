from django.contrib.auth.models import User
from django.db import models


class ProspectiveClient(models.Model):
    """
    Модель заполнения потенциальных клиентов, с назначением статуса
    клиенту и отметками о дате создания/изменения с указанием менеджера.

    Args:
        name (str): Имя клиента.
        email (str): Электронная почта клиента.
        description (str, optional): Описание клиента.
        status (str): Статус клиента.
        priority (str): Приоритет клиента.
        created_by (User): Менеджер, создавший запись.
        created_at (datetime): Время создания записи.
        modified_at (datetime): Время последнего изменения записи.
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
    WON = 'Назначен'
    LOST = 'Упущен'

    CHOICES_STATUS = (
        (NEW, 'Новый клиент'),
        (CONTACTED, 'Уже связались'),
        (WON, 'Назначен'),
        (LOST, 'Упущен'),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=45, choices=CHOICES_STATUS, default=NEW)
    priority = models.CharField(
        max_length=45, choices=CHOICES_PRIORITY, default=MEDIUM)
    created_by = models.ForeignKey(
        User, related_name='prospectiveclients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta():
        db_table = 'prospective_client'
        verbose_name = 'Потенциальный клиент'
        verbose_name_plural = 'Потенциальные клиенты'
