# Generated by Django 3.1.3 on 2021-04-09 00:54

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0064_auto_20210408_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='descripcion',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='Sin descripción', null=True),
        ),
    ]