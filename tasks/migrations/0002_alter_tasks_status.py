# Generated by Django 4.2.5 on 2024-12-17 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='status',
            field=models.CharField(choices=[(1, 'Done'), (2, 'Progressing'), (3, 'On Hold'), (4, 'Failed')], default=2, max_length=1),
        ),
    ]
