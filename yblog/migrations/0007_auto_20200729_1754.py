# Generated by Django 3.0.8 on 2020-07-29 08:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('yblog', '0006_auto_20200729_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 29, 8, 54, 1, 434273, tzinfo=utc)),
        ),
    ]
