# Generated by Django 3.1.3 on 2021-04-12 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0075_auto_20210410_1347'),
        ('Personas', '0009_clientes_email'),
        ('Store', '0012_auto_20210406_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favoritos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.productos')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Personas.usuariosweb')),
            ],
        ),
    ]
