# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-13 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0021_auto_20170711_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
