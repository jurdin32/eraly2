# Generated by Django 3.1.3 on 2020-11-26 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0025_auto_20201126_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='tipo_proveedor',
        ),
    ]
