# Generated by Django 3.1.3 on 2020-11-18 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0008_direccion_ciudad'),
        ('Producto', '0002_auto_20201117_1917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proveedor',
            name='ciudad',
        ),
        migrations.CreateModel(
            name='DireccionProveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(max_length=60)),
                ('telefono', models.CharField(max_length=10)),
                ('ciudad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.ciudad')),
            ],
        ),
        migrations.AddField(
            model_name='proveedor',
            name='direccion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Producto.direccionproveedor'),
        ),
    ]
