# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-01 23:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchresult',
            name='match',
        ),
        migrations.AddField(
            model_name='match',
            name='result',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='nalcs.MatchResult'),
            preserve_default=False,
        ),
    ]
