# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-20 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterbot', '0002_tweetresponseroundrobin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweetresponseroundrobin',
            name='last_index',
            field=models.PositiveIntegerField(default=0),
        ),
    ]