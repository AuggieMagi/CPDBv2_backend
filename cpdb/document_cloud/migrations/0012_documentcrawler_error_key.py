# Generated by Django 2.1.11 on 2019-11-13 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_cloud', '0011_documentcrawler_log_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentcrawler',
            name='error_key',
            field=models.CharField(max_length=255, null=True),
        ),
    ]