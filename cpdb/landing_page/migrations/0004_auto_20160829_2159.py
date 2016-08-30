# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-30 02:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0003_auto_20160829_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landingpage',
            name='faqs',
            field=models.ManyToManyField(to='faq.FAQPage'),
        ),
        migrations.AlterField(
            model_name='landingpage',
            name='stories',
            field=models.ManyToManyField(to='story.StoryPage'),
        ),
    ]
