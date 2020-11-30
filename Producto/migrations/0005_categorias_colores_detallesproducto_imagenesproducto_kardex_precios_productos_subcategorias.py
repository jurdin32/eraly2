# Generated by Django 3.1.3 on 2020-11-25 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0004_auto_20201119_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icono', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': '1. Categorias ',
            },
        ),
        migrations.CreateModel(
            name='Subcategorias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icono', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('categoria_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.categorias')),
            ],
            options={
                'verbose_name_plural': '2. Subcategorias ',
            },
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('talla', models.CharField(max_length=10)),
                ('dimension', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
                ('subcategoria_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.subcategorias')),
            ],
            options={
                'verbose_name_plural': '4. Producto ',
            },
        ),
        migrations.CreateModel(
            name='Precios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precioVenta', models.DecimalField(decimal_places=2, max_digits=5)),
                ('detalle', models.CharField(max_length=50)),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.productos')),
            ],
            options={
                'verbose_name_plural': '6. Color Producto ',
            },
        ),
        migrations.CreateModel(
            name='Kardex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('cantidad', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=150)),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.productos')),
            ],
            options={
                'verbose_name_plural': '7. Kardex ',
            },
        ),
        migrations.CreateModel(
            name='ImagenesProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, help_text='100x100', null=True, upload_to='producto')),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.productos')),
            ],
            options={
                'verbose_name_plural': '8. Imagenes de Producto ',
            },
        ),
        migrations.CreateModel(
            name='DetallesProducto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icono', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('categoria_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.categorias')),
            ],
            options={
                'verbose_name_plural': '3. Detalles del Producto ',
            },
        ),
        migrations.CreateModel(
            name='Colores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('codigoColor', models.CharField(max_length=50)),
                ('producto_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Producto.productos')),
            ],
            options={
                'verbose_name_plural': '5. Color Producto ',
            },
        ),
    ]