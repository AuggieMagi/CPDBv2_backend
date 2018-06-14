# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-18 01:53
from __future__ import unicode_literals
from contextlib import contextmanager
from csv import DictReader
import os
from tempfile import NamedTemporaryFile

from django.conf import settings
from django.db import migrations

from azure.storage.blob import BlockBlobService


@contextmanager
def csv_from_azure(filename):
    block_blob_service = BlockBlobService(
        account_name=settings.DATA_PIPELINE_STORAGE_ACCOUNT_NAME,
        account_key=settings.DATA_PIPELINE_STORAGE_ACCOUNT_KEY
    )
    tmp_file = NamedTemporaryFile(suffix='.csv', delete=False)
    block_blob_service.get_blob_to_path('csv', filename, tmp_file.name)
    csvfile = open(tmp_file.name)
    reader = DictReader(csvfile)
    yield reader
    csvfile.close()
    os.remove(tmp_file.name)


def import_officers_data(apps, schema_editor):
    with csv_from_azure('20180518_officer.csv') as reader:
        pks = []

        Officer = apps.get_model('data', 'Officer')
        blank_or_null = {
            field.name: None if field.null else ''
            for field in Officer._meta.get_fields()
        }
        for row in reader:
            for key, val in row.iteritems():
                if val == '':
                    row[key] = blank_or_null[key]
            pks.append(int(row['pk']))
            officer, created = Officer.objects.update_or_create(
                id=int(row['pk']),
                defaults={
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'middle_initial': row['middle_initial'],
                    'middle_initial2': row['middle_initial2'],
                    'suffix_name': row['suffix_name'],
                    'gender': row['gender'],
                    'race': row['race'],
                    'appointed_date': row['appointed_date'],
                    'resignation_date': row['resignation_date'],
                    'rank': row['rank'],
                    'birth_year': row['birth_year'],
                    'active': row['active']
                }
            )

    Officer.objects.exclude(pk__in=pks).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0037_import_policeunit_data'),
    ]

    operations = [
        migrations.RunPython(
            import_officers_data,
            reverse_code=migrations.RunPython.noop,
            elidable=True),
    ]