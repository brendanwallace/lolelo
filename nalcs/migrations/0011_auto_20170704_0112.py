# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-04 01:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nalcs', '0010_match_game_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('match_wins', models.IntegerField()),
                ('match_losses', models.IntegerField()),
                ('game_wins', models.IntegerField()),
                ('game_losses', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='predictions',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='nalcs.TeamStats'),
            preserve_default=False,
        ),
    ]
