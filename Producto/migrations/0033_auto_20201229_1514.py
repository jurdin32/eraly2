# Generated by Django 3.1.3 on 2020-12-29 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0032_auto_20201229_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productos',
            old_name='Marca',
            new_name='marca',
        ),
    ]
