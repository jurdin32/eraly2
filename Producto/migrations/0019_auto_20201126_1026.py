# Generated by Django 3.1.3 on 2020-11-26 15:26

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0018_auto_20201126_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='detallesTecnicos',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productos',
            name='descripcion',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
