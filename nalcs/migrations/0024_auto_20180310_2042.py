# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-10 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0023_auto_20170714_2116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='spring_championship_points',
        ),
        migrations.AddField(
            model_name='team',
            name='short',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
