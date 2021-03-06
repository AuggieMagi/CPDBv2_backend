# Generated by Django 2.1.3 on 2019-02-22 05:25

from django.db import migrations
from django.db.models import OuterRef, Subquery, Count, IntegerField


class SQCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0114_attachmentfile_add_fields'),
    ]

    def populate_notifications_count(apps, schema_editor):
        AttachmentFile = apps.get_model('data', 'AttachmentFile')
        AttachmentRequest = apps.get_model('data', 'AttachmentRequest')

        AttachmentFile.objects.update(
            notifications_count=SQCount(
                AttachmentRequest.bulk_objects.filter(
                    noti_email_sent=True,
                    allegation_id=OuterRef('allegation_id')
                ).values('id')
            )
        )

    operations = [
        migrations.RunPython(
            populate_notifications_count,
            reverse_code=migrations.RunPython.noop,
            elidable=True),
    ]
