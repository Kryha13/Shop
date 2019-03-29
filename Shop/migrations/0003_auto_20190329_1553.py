# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-29 15:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0002_auto_20190328_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_deadline',
            field=models.DateField(verbose_name=datetime.date(2019, 4, 5)),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/media/'),
        ),
    ]