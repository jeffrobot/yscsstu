# Generated by Django 3.0.8 on 2020-07-29 07:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('yblog', '0003_auto_20200729_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 29, 7, 19, 1, 982875, tzinfo=utc)),
        ),
    ]
