# Generated by Django 3.1.3 on 2020-11-26 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0014_auto_20201126_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marca',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='marca/imagenes'),
        ),
    ]
