# Generated by Django 3.1.3 on 2021-03-25 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0055_auto_20210325_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagenesproducto',
            name='thumbails',
            field=models.ImageField(blank=True, null=True, upload_to='producto'),
        ),

    ]
