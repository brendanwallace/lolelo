# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-02 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0003_match_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='date',
            field=models.DateField(),
            preserve_default=False,
        ),
    ]