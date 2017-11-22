# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-01 08:23
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_reportpage_officers'),
    ]

    operations = [
        migrations.AddField(
            model_name='faqpage',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20, null=True), default=[], size=None),
        ),
        migrations.AddField(
            model_name='reportpage',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20, null=True), default=[], size=None),
        ),
    ]