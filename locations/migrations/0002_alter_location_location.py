# Generated by Django 3.2.5 on 2021-08-06 00:47

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=(0.0, 0.0), srid=4326),
        ),
    ]