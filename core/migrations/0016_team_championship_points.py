# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-06 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_team_win_split'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='championship_points',
            field=models.IntegerField(default=0),
        ),
    ]
