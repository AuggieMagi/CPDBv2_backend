# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-31 03:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0028_merge'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('faq', '0004_migrate_data_from_faqpage_to_faq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faqpage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='FAQPage',
        ),
    ]
