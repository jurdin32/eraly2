# Generated by Django 3.1.3 on 2021-03-24 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0049_productos_puntuacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='precios',
            name='web',
            field=models.BooleanField(default=False),
        ),
    ]