# Generated by Django 3.1.3 on 2021-01-20 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Empresa', '0007_auto_20201125_1804'),
        ('Ventas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturas',
            name='establecimiento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Empresa.establecimiento'),
        ),
    ]
