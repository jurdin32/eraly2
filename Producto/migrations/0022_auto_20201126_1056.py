# Generated by Django 3.1.3 on 2020-11-26 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0021_auto_20201126_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kardex',
            name='descripcion',
            field=models.TextField(),
        ),
    ]