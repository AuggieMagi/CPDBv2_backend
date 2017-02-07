class Formatter(object):
    def format(self):
        raise NotImplementedError


class SimpleFormatter(Formatter):
    def doc_format(self, doc):
        return doc.to_dict()

    def format(self, response):
        return [self.doc_format(doc) for doc in response.hits]


class OfficerFormatter(SimpleFormatter):
    def doc_format(self, doc):
        return {
            'text': doc.full_name,
            'payload': {
                'result_text': doc.full_name,
                'result_extra_information': doc.badge and 'Badge # {badge}'.format(badge=doc.badge) or '',
                'url': doc.url
            }
        }


class NameFormatter(SimpleFormatter):
    def doc_format(self, doc):
        return {
            'text': doc.name,
            'payload': {
                'result_text': doc.name,
                'url': doc.url
            }
        }


class OfficerV2Formatter(SimpleFormatter):
    def doc_format(self, doc):
        return {
            'result_text': doc.full_name,
            'result_extra_information': doc.badge and 'Badge # {badge}'.format(badge=doc.badge) or '',
            'url': doc.url
        }


class NameV2Formatter(SimpleFormatter):
    def doc_format(self, doc):
        return {
            'result_text': doc.name,
            'url': doc.url
        }


class FAQFormatter(SimpleFormatter):
    def doc_format(self, doc):
        return {
            'question': doc.question,
            'answer': doc.answer
        }


class ReportFormatter(SimpleFormatter):
    def doc_format(self, doc):
        return {
            'publication': doc.publication,
            'author': doc.author,
            'title': doc.title,
            'excerpt': doc.excerpt
        }


class CoAccusedOfficerFormatter(Formatter):
    def doc_format(self, doc):
        return {
            'text': doc['full_name'],
            'payload': {
                'url': doc['url'],
                'result_text': doc['full_name'],
                'result_extra_information': doc['badge'] and 'Badge # {badge}'.format(badge=doc['badge']) or ''
            }
        }

    def format(self, response):
        docs = []
        for hit in response.hits:
            docs += hit.co_accused_officer

        return [self.doc_format(doc) for doc in docs]
