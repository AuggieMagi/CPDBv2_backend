# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-25 09:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_reportpage_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='slugpage',
            old_name='descriptor_class',
            new_name='serializer_class',
        ),
        migrations.RemoveField(
            model_name='reportpage',
            name='descriptor_class',
        ),
    ]
