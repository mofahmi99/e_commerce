# Generated by Django 3.2.5 on 2021-08-26 12:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_orderproduct_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(blank=True, default=datetime.date(2021, 8, 26), null=True),
        ),
    ]