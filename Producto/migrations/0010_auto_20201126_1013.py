# Generated by Django 3.1.3 on 2020-11-26 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0007_auto_20201125_1804'),
        ('Producto', '0009_auto_20201126_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorias',
            name='establecimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresa.establecimiento'),
        ),
        migrations.AddField(
            model_name='productos',
            name='establecimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresa.establecimiento'),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='establecimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresa.establecimiento'),
        ),
    ]
