# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-31 10:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='adress',
        ),
    ]
