# Generated by Django 4.1.3 on 2022-12-03 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='completada',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]