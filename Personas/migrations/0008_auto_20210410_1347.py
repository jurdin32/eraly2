# Generated by Django 3.1.3 on 2021-04-10 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0007_auto_20210331_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariosweb',
            name='identificacion',
            field=models.CharField(max_length=13),
        ),
    ]
