# Generated by Django 3.1.3 on 2021-04-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0011_detallecompraweb_enviado'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallecompraweb',
            name='etiqueta',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='detallecompraweb',
            name='enviado',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
