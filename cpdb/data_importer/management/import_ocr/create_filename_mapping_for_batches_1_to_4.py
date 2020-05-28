import csv
from urllib.request import urlopen
from io import StringIO
from tqdm import tqdm
from django.conf import settings

from data.models import *
from documentcloud import DocumentCloud


ocr_file_url = 'https://ucf3a8d9b0919a1fa2f8e2c7c35d.dl.dropboxusercontent.com/cd/0/get/A5BafmifnvtZ0lN1h6xWKda_zS1YYssUjSxbqbXhr0Yfdgm7iSzxwl2yAOupbNyZEUNcjkQn4bettDs4SN-Ul_yi5OsUmJWgbR_jSubGpHCfb0PenPZsleZQ89w19trZayY/file#'
first_batch_csv_url = 'https://uc13a6ce560243ad8e63e5aed697.dl.dropboxusercontent.com/cd/0/get/A5AqGZnJAhNm0cTwnHlzNR8AcNViC_7BADowwAswKsRvpjV1cyj8eXU7PJvsMCCxUS3-gXBcTaxKt522LsHB2PJwgmyJZSeSXJzfKDeA1-qIebWPtXUipFUEZGv-dCnl69M/file#'
third_batch_csv_url = 'https://uc9940356bfc491b2332eab16cc4.dl.dropboxusercontent.com/cd/0/get/A5BEW-KjWznhxAokpukM4DIPwDhOxy-I0pHDBFPKGCzxnLHhUmeTnVnQ3IjtOYjnO34Z_cItx_o9Z4otbs4aO_2fFGClFqnpl2oOT0EDQ_T7PLFDrUzakYmhWigsy_HacO0/file#'

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

ocr_csv_file = read_remote_csv(ocr_file_url)
data = set()
for crid, file_name, _, batch_name, _, _ in ocr_csv_file[1:]:
    data.add((crid, file_name, batch_name))

data = [list(row) for row in data]

first_batch_csv_file = read_remote_csv(first_batch_csv_url)
third_batch_csv_file = read_remote_csv(third_batch_csv_url)

first_batch_mapping = create_mapping(first_batch_csv_file)
third_batch_mapping = create_mapping(third_batch_csv_file)


client = DocumentCloud(settings.DOCUMENTCLOUD_USER, settings.DOCUMENTCLOUD_PASSWORD)

cloud_documents = []
missing_cloud_documents = []
missing_attachments = []
results = []


for crid, file_name, batch_name in tqdm(data):
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
        continue
    if attachment:
        results.append([file_name, attachment.url, batch_name])
    else:
        missing_attachments.append([crid, file_name, batch_name])


missing_cloud_documents = [
    ['1053568', 'CPD 0043808.pdf', 'https://assets.documentcloud.org/documents/6754053/CRID-1053568-CR-Summary.pdf', 'Green 2019_12_30 Production'],
    ['1053568', 'CPD 0043811.pdf', 'https://assets.documentcloud.org/documents/6756712/CRID-1053568-CR-Face-Sheet.pdf', 'Green 2019_12_30 Production'],
    ['1054847', 'CPD 0048431.pdf', 'https://assets.documentcloud.org/documents/6751433/CRID-1054847-CR-Face-Sheet.pdf', 'Green 2019_12_30 Production'],
    ['1054847', 'CPD 0048429.pdf', 'https://assets.documentcloud.org/documents/6754651/CRID-1054847-CR-Summary.pdf', 'Green 2019_12_30 Production'],
    ['1053568', 'CPD 0043815.pdf', 'https://assets.documentcloud.org/documents/6757351/CRID-1053568-CR-Attachment-DOCID-845457.pdf', 'Green 2019_12_30 Production'],
    ['1051619', 'LOG_1051619.pdf', 'https://assets.documentcloud.org/documents/6764483/CRID-1051619-DOCUMENT-LOG-1051619.pdf', 'Green 2020_01_31 Production'],
    ['1053568', 'CPD 0043812.pdf', 'https://assets.documentcloud.org/documents/6756242/CRID-1053568-CR-Attachment-DOCID-845454.pdf', 'Green 2019_12_30 Production'],
    ['1054755', 'CPD 0048171.pdf', 'https://assets.documentcloud.org/documents/6754524/CRID-1054755-CR-Summary.pdf', 'Green 2019_12_30 Production'],
    ['1054755', 'CPD 0048174.pdf', 'https://assets.documentcloud.org/documents/6758652/CRID-1054755-CR-Face-Sheet.pdf', 'Green 2019_12_30 Production']
]

for _, file_name, doc_url, batch_name in missing_cloud_documents:
    results.append([file_name, doc_url, batch_name])

with open('filename_mapping.csv', 'wt') as f:
    writer = csv.writer(f)

    writer.writerow(['filename', 'doccloud_url', 'batch_name'])
    writer.writerows(results)
