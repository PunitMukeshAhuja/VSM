# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-22 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0018_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='profit_on_current',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='profit_on_transact',
            field=models.FloatField(default=0.0),
        ),
    ]