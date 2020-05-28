import csv
from urllib.request import urlopen
from io import StringIO
from tqdm import tqdm
from django.db.models import Prefetch

from data.models import *

# Dropbox links
ocr_file_url = 'ocr_text.csv?dl=1'
first_batch_csv_url = 'green-2019-09-03-file-names.csv?dl=1'
third_batch_csv_url = 'green-2019-12-30-file-names.csv?dl=1'


def read_remote_csv(url):
    ftp_stream = urlopen(url)
    text = ftp_stream.read().decode('utf-8')
    csv_file = csv.reader(StringIO(text), delimiter=',')
    return list(csv_file)


def create_mapping(csv_file):
    mapping = {}
    for file_name, file_title in csv_file[1:]:
        mapping[file_name] = file_title
    return mapping


ocr_csv_file = read_remote_csv(ocr_file_url)[1:]
sorted_ocr_csv_file = list(sorted(ocr_csv_file, key=lambda row: row[1] + '_' + row[2]))
first_batch_csv_file = read_remote_csv(first_batch_csv_url)
third_batch_csv_file = read_remote_csv(third_batch_csv_url)

first_batch_mapping = create_mapping(first_batch_csv_file)
third_batch_mapping = create_mapping(third_batch_csv_file)

file_name_in_db = []
file_name_not_in_db = []
attachment_ocrs = []

for crid, file_name, page_num, batch_name, doc_url, ocr_text in tqdm(sorted_ocr_csv_file):
    attachment = None
    if '2019_09_03' in batch_name:
        file_title = first_batch_mapping.get(file_name.replace('.pdf', ''))
        if file_title:
            attachment = AttachmentFile.objects.filter(allegation_id=crid, title__contains=file_title).first()
    elif '2019_12_02' in batch_name:
        attachment = AttachmentFile.objects.filter(allegation_id=crid, url__contains=file_name.replace('_', '-').replace(' ', '-')).first()
    elif '2019_12_30' in batch_name:
        file_title = third_batch_mapping.get(file_name.replace('.pdf', ''))
        if file_title:
            attachment = AttachmentFile.objects.filter(allegation_id=crid, title__contains=file_title).first()
    elif '2020_01_31' in batch_name:
        attachment = AttachmentFile.objects.filter(allegation_id=crid, url__contains=file_name.replace('_', '-').replace(' ', '-')).first()
    else:
        attachment = AttachmentFile.objects.filter(allegation_id=crid, url=doc_url).first()

    if attachment:
        file_name_in_db.append((file_name, batch_name))
    else:
        file_name_not_in_db.append((file_name, batch_name))

    if attachment:
        attachment_ocrs.append(AttachmentOCR(attachment=attachment, page_num=page_num, ocr_text=ocr_text))

    if len(attachment_ocrs) == 5000:
        AttachmentOCR.objects.bulk_create(attachment_ocrs, batch_size=1000)
        attachment_ocrs = []

AttachmentOCR.objects.bulk_create(attachment_ocrs, batch_size=1000)

attachment_ids = AttachmentOCR.objects.values_list('attachment_id').distinct()
attachments = AttachmentFile.objects.filter(id__in=attachment_ids).prefetch_related(Prefetch('attachment_ocrs', queryset=AttachmentOCR.objects.order_by('page_num')))

for attachment in tqdm(attachments):
    attachment.text_content = '\n'.join([attachment_ocr.ocr_text for attachment_ocr in attachment.attachment_ocrs.all()])
    attachment.is_external_ocr = True

AttachmentFile.objects.bulk_update(
    attachments, update_fields=['is_external_ocr', 'text_content'], batch_size=1000
)

print('In DB', len(set(file_name_in_db)))
print('Not in DB', len(set(file_name_not_in_db)))
