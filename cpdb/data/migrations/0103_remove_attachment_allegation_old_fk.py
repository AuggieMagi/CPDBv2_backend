# Generated by Django 2.1.3 on 2019-01-08 03:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0102_change_attachment_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachmentfile',
            name='allegation_old_fk',
        ),
        migrations.RemoveField(
            model_name='attachmentrequest',
            name='allegation_old_fk',
        ),
    ]