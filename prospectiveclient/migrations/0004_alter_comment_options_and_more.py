# Generated by Django 4.2.11 on 2024-05-18 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prospectiveclient', '0003_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Коментарий для потенциального клиента', 'verbose_name_plural': 'Коментарии для потенциальных клиентов'},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='lead',
            new_name='prospectiveclient',
        ),
    ]
