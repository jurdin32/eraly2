# Generated by Django 3.1.3 on 2021-04-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0004_comprasweb_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprasweb',
            name='fecha',
            field=models.DateTimeField(auto_created=True, blank=True, null=True),
        ),
    ]
