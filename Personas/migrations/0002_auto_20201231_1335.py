# Generated by Django 3.1.3 on 2020-12-31 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='celular',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='clientes',
            name='telefono',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
