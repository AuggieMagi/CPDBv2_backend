# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterbot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetResponseRoundRobin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=15)),
                ('response_type', models.CharField(choices=[[b'single_officer', b'Single Officer'], [b'coaccused_pair', b'Coaccused Pair'], [b'not_found', b'Not Found']], max_length=20)),
                ('last_index', models.PositiveIntegerField()),
            ],
        ),
    ]
