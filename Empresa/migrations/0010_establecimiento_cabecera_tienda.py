# Generated by Django 3.1.3 on 2021-02-26 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0009_auto_20210223_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='establecimiento',
            name='cabecera_tienda',
            field=models.ImageField(blank=True, null=True, upload_to='logos/tienda'),
        ),
    ]