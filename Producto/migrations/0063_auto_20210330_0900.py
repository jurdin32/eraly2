# Generated by Django 3.1.3 on 2021-03-30 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0062_auto_20210325_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, default='noimagen.jpg', null=True, upload_to='productos'),
        ),
    ]