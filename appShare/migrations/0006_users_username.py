# Generated by Django 4.2 on 2023-06-19 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appShare', '0005_rename_servicios_citasservicios_serviciosid'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='username',
            field=models.CharField(default='', max_length=80),
        ),
    ]