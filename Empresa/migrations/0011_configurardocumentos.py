# Generated by Django 3.1.3 on 2021-03-13 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0010_establecimiento_cabecera_tienda'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigurarDocumentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proformas', models.IntegerField(default=1)),
                ('facturas', models.IntegerField(default=1)),
                ('establecimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresa.establecimiento')),
            ],
        ),
    ]
