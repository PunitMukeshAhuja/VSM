# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-13 12:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('price', '0007_auto_20170913_1715'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserInfo',
            new_name='Profile',
        ),
    ]
