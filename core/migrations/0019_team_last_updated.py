# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-07 03:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_team_spring_championship_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
