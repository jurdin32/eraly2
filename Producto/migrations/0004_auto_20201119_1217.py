# Generated by Django 3.1.3 on 2020-11-19 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0003_auto_20201117_1927'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='direccion',
        ),
        migrations.AddField(
            model_name='direccionproveedor',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Producto.proveedor'),
        ),
    ]
