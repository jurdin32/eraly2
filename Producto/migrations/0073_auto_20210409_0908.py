# Generated by Django 3.1.3 on 2021-04-09 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0072_productos_etiquetas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='tipo',
            field=models.CharField(default='P', max_length=20),
        ),
    ]
