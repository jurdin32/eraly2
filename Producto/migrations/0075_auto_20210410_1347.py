# Generated by Django 3.1.3 on 2021-04-10 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0074_remove_categorias_establecimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos'),
        ),
    ]
