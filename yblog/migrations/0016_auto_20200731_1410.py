# Generated by Django 3.0.8 on 2020-07-31 05:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('yblog', '0015_auto_20200731_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 31, 5, 10, 19, 317939, tzinfo=utc)),
        ),
    ]
