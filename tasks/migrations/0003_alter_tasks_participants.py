# Generated by Django 4.2.5 on 2024-12-17 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_alter_tasks_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='participants',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
