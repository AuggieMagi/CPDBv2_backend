# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-11-02 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0086_allegation_subjects'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachmentfile',
            name='source_type',
            field=models.CharField(db_index=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attachmentfile',
            name='external_id',
            field=models.CharField(db_index=True, max_length=255, null=True),
        )
    ]
