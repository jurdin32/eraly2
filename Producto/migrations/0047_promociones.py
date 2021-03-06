# Generated by Django 3.1.3 on 2021-03-24 01:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0046_auto_20210323_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promociones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.DateField()),
                ('fechaFinal', models.DateField()),
                ('descuento', models.IntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('precio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.precios')),
            ],
        ),
    ]
