# Generated by Django 2.1.3 on 2018-11-23 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitterbot', '0005_twitterbotresponselog_original_event_object'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsetemplate',
            name='response_type',
            field=models.CharField(choices=[['single_officer', 'Single Officer'], ['coaccused_pair', 'Coaccused Pair'], ['not_found', 'Not Found']], max_length=20),
        ),
        migrations.AlterField(
            model_name='tweetresponseroundrobin',
            name='response_type',
            field=models.CharField(choices=[['single_officer', 'Single Officer'], ['coaccused_pair', 'Coaccused Pair'], ['not_found', 'Not Found']], max_length=20),
        ),
        migrations.AlterField(
            model_name='twitterbotresponselog',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SENT', 'Sent')], default='PENDING', max_length=10),
        ),
    ]
