# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-11 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0019_team_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='date',
            field=models.DateField(null=True),
        ),
    ]