# Generated by Django 3.1.3 on 2021-04-11 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0012_establecimiento_color_encabezado_documentos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioempresa',
            name='cedula',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]