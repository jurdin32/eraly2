# Generated by Django 3.1.3 on 2021-01-27 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Personas', '0003_clientes_establecimiento'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
