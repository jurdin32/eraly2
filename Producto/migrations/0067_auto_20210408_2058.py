# Generated by Django 3.1.3 on 2021-04-09 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0066_auto_20210408_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='subcategoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Producto.categorias'),
        ),
    ]
