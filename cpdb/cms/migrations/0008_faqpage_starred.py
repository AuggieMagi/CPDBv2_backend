# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-19 03:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_faqpage_order_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqpage',
            name='starred',
            field=models.BooleanField(default=False),
        ),
    ]
