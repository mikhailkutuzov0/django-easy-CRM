# Generated by Django 4.2.11 on 2024-05-18 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='prospectiveclient',
            new_name='client',
        ),
    ]
