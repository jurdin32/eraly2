# Generated by Django 3.1.3 on 2021-04-09 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0065_auto_20210408_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorias',
            name='icono',
        ),
        migrations.AddField(
            model_name='categorias',
            name='principal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Producto.categorias'),
        ),
    ]
