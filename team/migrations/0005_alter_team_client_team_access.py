# Generated by Django 4.2.11 on 2024-05-19 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_alter_team_client_team_access'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='client_team_access',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='team.clientteamaccess', verbose_name='Доступ к клиентам'),
        ),
    ]
