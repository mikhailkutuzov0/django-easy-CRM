from django.contrib.auth.models import User
from django.db import models


class ProspectiveClient(models.Model):
    """
    Модель заполнения потенциальных клиентов, с назначением статуса
    клиенту и отметками о дате создания/изменения с указанием менеджера.

    Args:
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

    def __str__(self):
        return f'{self.name} | {self.status} | {self.priority}'
