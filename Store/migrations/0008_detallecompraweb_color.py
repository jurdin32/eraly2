# Generated by Django 3.1.3 on 2021-04-03 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_auto_20210403_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallecompraweb',
            name='color',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
