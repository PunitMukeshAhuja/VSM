# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-17 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0016_auto_20170915_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance_shares',
            field=models.IntegerField(default=0),
        ),
    ]
