# Generated by Django 4.1 on 2022-09-08 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yumyum', '0013_alter_category_update_at_last_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='update_at_last_news',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 8, 10, 51, 50, 155452)),
        ),
    ]
