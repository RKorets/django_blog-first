# Generated by Django 4.1 on 2022-08-21 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yumyum', '0009_sex_remove_customuserregistration_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='update_at_last_news',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 21, 11, 46, 33, 306497)),
        ),
    ]
