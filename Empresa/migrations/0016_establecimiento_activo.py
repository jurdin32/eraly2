# Generated by Django 3.1.3 on 2021-04-13 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0015_auto_20210411_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]