# Generated by Django 3.1.3 on 2021-01-27 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0011_delete_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurarDocumentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proformas', models.CharField(max_length=13)),
                ('facturas', models.CharField(max_length=13)),
            ],
        ),
    ]
