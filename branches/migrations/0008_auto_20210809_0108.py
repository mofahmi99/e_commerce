# Generated by Django 3.2.5 on 2021-08-09 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0007_auto_20210809_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='branchitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='branchitem',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
