import csv
from urllib.request import urlopen
from io import StringIO
from tqdm import tqdm

from data.models import *

# Dropbox links
narrative_csv_url = 'narratives.csv?dl=1'
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


narrative_csv_file = read_remote_csv(narrative_csv_url)[1:]
sorted_narrative_csv_file = list(sorted(narrative_csv_file, key=lambda row: row[1] + '_' + row[2]))
first_batch_csv_file = read_remote_csv(first_batch_csv_url)
third_batch_csv_file = read_remote_csv(third_batch_csv_url)

first_batch_mapping = create_mapping(first_batch_csv_file)
third_batch_mapping = create_mapping(third_batch_csv_file)

file_name_in_db = []
file_name_not_in_db = []
attachment_narratives = []

for crid, file_name, page_num, section_name, column_name, text_content, _, batch_name, doc_url in tqdm(sorted_narrative_csv_file):
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
        file_name_in_db.append((crid, file_name, batch_name))
    else:
        file_name_not_in_db.append((crid, file_name, batch_name))

    if attachment:
        attachment_narratives.append(
            AttachmentNarrative(
                attachment=attachment,
                page_num=page_num,
                section_name=section_name,
                column_name=column_name,
                text_content=text_content
            )
        )

AttachmentNarrative.objects.bulk_create(attachment_narratives)

print('In DB', len(set(file_name_in_db)))
print('Not in DB', len(set(file_name_not_in_db)))

