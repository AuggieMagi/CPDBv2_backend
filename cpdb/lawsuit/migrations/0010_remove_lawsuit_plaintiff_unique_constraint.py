# Generated by Django 2.2.10 on 2020-08-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lawsuit', '0009_change_lawsuit_location_max_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawsuitplaintiff',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]