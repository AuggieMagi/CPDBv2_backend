# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-30 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailcore', '0028_merge'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('faq', '0003_faqspage'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('body', wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.TextBlock())])),
            ],
        ),
        migrations.RemoveField(
            model_name='faqspage',
            name='page_ptr',
        ),
        migrations.DeleteModel(
            name='FAQsPage',
        ),
    ]
