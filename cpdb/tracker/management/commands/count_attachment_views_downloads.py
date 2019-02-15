import logging

from django.core.management.base import BaseCommand

from tqdm import tqdm

from data.models import AttachmentFile
from analytics.models import Event

logger = logging.getLogger('attachment.count_views_and_downloads')


class Command(BaseCommand):
    help = "Count attachments views and downloads"

    def handle(self, *args, **kwargs):
        for attachment in tqdm(AttachmentFile.objects.all(), desc='Updating attachments'):
            attachment.views_count = Event.objects.filter(name='attachment-view', data__id=attachment.id).count()
            attachment.downloads_count = Event.objects.filter(
                name='attachment-download', data__id=attachment.id
            ).count()
            attachment.save()
