# Generated by Django 3.2.5 on 2021-08-29 23:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_orderproduct_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 8, 29, 23, 8, 40, 278333, tzinfo=utc), null=True),
        ),
    ]
