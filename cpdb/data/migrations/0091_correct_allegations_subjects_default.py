# Generated by Django 2.1.3 on 2018-11-30 03:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0090_merge_20181129_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allegation',
            name='subjects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), default=list, size=None),
        ),
    ]
