# Generated by Django 3.1.3 on 2021-01-28 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0036_auto_20210122_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorias',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='categorias',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='subcategorias',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]