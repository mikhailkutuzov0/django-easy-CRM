# Generated by Django 4.2.11 on 2024-05-18 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_alter_team_client_team_access'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prospectiveclient', '0002_alter_prospectiveclient_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Содержание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано в')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prospectiveclients_comments', to=settings.AUTH_USER_MODEL, verbose_name='Создано кем')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='prospectiveclient.prospectiveclient', verbose_name='Кто оставил комментарий')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prospectiveclients_comments', to='team.team', verbose_name='Коментарий для потенциального клиента')),
            ],
            options={
                'verbose_name': 'Коментарий для потенциального клиента',
                'verbose_name_plural': 'Коментариb для потенциальных клиентов',
                'db_table': 'prospective_client_comment',
            },
        ),
    ]
