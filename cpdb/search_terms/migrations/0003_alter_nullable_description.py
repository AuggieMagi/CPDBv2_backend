# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-20 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search_terms', '0002_add_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchtermitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
