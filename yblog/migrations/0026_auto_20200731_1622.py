# Generated by Django 3.0.8 on 2020-07-31 07:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('yblog', '0025_auto_20200731_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 31, 7, 22, 3, 459778, tzinfo=utc)),
        ),
    ]
