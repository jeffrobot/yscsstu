# Generated by Django 3.0.8 on 2020-07-29 15:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('yblog', '0009_auto_20200730_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 29, 15, 7, 42, 215471, tzinfo=utc)),
        ),
    ]
