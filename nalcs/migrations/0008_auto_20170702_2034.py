# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-02 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0007_auto_20170702_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchresult',
            name='match',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nalcs.Match'),
        ),
    ]
