# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-25 02:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_create_report_page_rename_cms_page_to_slug_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportpage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 10, 24, 21, 9, 46, 226482)),
            preserve_default=False,
        ),
    ]