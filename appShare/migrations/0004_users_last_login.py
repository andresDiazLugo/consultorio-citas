# Generated by Django 4.2 on 2023-06-11 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appShare', '0003_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
    ]
