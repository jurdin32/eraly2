# Generated by Django 3.1.3 on 2020-11-18 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruc', models.CharField(max_length=10)),
                ('nombreComercial', models.CharField(max_length=60)),
                ('direccion', models.CharField(max_length=60)),
            ],
        ),
    ]