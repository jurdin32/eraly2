# Generated by Django 3.1.3 on 2020-11-30 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0027_auto_20201126_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallesproducto',
            name='precioCompra',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]