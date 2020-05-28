from django.conf import settings
from re import match
from tqdm import tqdm

from documentcloud import DocumentCloud


client = DocumentCloud(settings.DOCUMENTCLOUD_USER, settings.DOCUMENTCLOUD_PASSWORD)
all_documents = client.documents.search('projectid:49649', data=True)

pattern = r'^CRID \d+$'
for document in tqdm(all_documents):
    if match(pattern, document.title):
        original_filename = document.data['filename'].replace('.pdf', '')
        document.title = f'{document.title} {original_filename}'
        document.save()


client = DocumentCloud(settings.DOCUMENTCLOUD_USER, settings.DOCUMENTCLOUD_PASSWORD)
all_documents = client.documents.search('account:23814-matt-chapman title:crid', data=True)

pattern = r'^CRID \d+$'
for document in tqdm(all_documents):
    if match(pattern, document.title) and not document.data and document.access == 'public':
        document.delete()


all_documents = client.documents.search('projectid:49649', data=True)

deleted_batches = ['2019.09.03', '2019.12.02', '2019.12.30', '2020.01.31']

deleted_documents = []
for document in tqdm(all_documents):
    if any([batch in document.data['batch'] for batch in deleted_batches]) and document.access == 'public':
        deleted_documents.append(document)

for d in tqdm(deleted_documents):
    d.delete()
