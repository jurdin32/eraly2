# Generated by Django 3.1.3 on 2021-03-25 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):


    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Producto', '0054_auto_20210325_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calificacionproductos',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.productos'),
        ),
        migrations.AlterField(
            model_name='calificacionproductos',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
