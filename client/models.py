from django.contrib.auth.models import User
from django.db import models
from team.models import Team


class Client(models.Model):
    """
    Модель для представления клиента.

    Attributes:
        team (ForeignKey): Ссылка на команду, к которой относится клиент.
        name (CharField): Имя клиента.
        email (EmailField): Электронная почта клиента.
        description (TextField): Описание клиента.
        created_by (ForeignKey): Пользователь, создавший запись о клиенте.
        created_at (DateTimeField): Дата и время создания записи.
        modified_at (DateTimeField): Дата и время последнего изменения записи.
    """
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


class ClientFile(models.Model):
    """
    Модель для представления файла клиента.

    Attributes:
        team (ForeignKey): Ссылка на команду клиента.
        client (ForeignKey): Ссылка на клиента, для которого загружается файл.
        file (FileField): Загружаемый файл.
        created_by (ForeignKey): Пользователь, загрузивший файл.
        created_at (DateTimeField): Дата и время загрузки файла.
    """
    team = models.ForeignKey(
        Team,
        related_name='clients_files',
        on_delete=models.CASCADE,
        verbose_name='Команда клиента'
    )
    client = models.ForeignKey(
        Client,
        related_name='files',
        on_delete=models.CASCADE,
        verbose_name='Для кого оставлен файл'
    )
    file = models.FileField(
        upload_to='clients_files',
        verbose_name='Файл'
    )
    created_by = models.ForeignKey(
        User,
        related_name='clients_files',
        on_delete=models.CASCADE,
        verbose_name='Загружено кем'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Создано в')

    class Meta():
        db_table = 'client_files'
        verbose_name = 'Файл для клиента'
        verbose_name_plural = 'Файлы для клиентов'

    def __str__(self):
        return f'{self.created_by} - {self.file}'


class Comment(models.Model):
    """
    Модель для представления комментария к клиенту.

    Attributes:
        team (ForeignKey): Ссылка на команду клиента.
        client (ForeignKey): Ссылка на клиента, для которого оставлен комментарий.
        content (TextField): Содержание комментария.
        created_by (ForeignKey): Пользователь, создавший комментарий.
        created_at (DateTimeField): Дата и время создания комментария.
    """
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
