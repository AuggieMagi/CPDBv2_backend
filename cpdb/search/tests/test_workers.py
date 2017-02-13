from django.test import SimpleTestCase

from robber import expect

from search.workers import (
        FAQWorker, ReportWorker, OfficerWorker, UnitWorker, UnitOfficerWorker,
        NeighborhoodsWorker, CommunityWorker, CoAccusedOfficerWorker)
from search.doc_types import (
        FAQDocType, ReportDocType, OfficerDocType, UnitDocType, UnitOfficerDocType,
        NeighborhoodsDocType, CommunityDocType, CoAccusedOfficerDocType)
from search.tests.utils import IndexMixin


class FAQWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = FAQDocType(question='question', answer='answer')
        doc.save()

        self.refresh_index()

        response = FAQWorker().search('question')
        expect(response.hits.total).to.be.equal(1)


class ReportWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = ReportDocType(
            publication='publication', title='title',
            author='author', excerpt='excerpt')
        doc.save()

        self.refresh_index()

        response = ReportWorker().search('author')
        expect(response.hits.total).to.be.equal(1)


class OfficerWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = OfficerDocType(
            full_name='full name', badge='123')
        doc.save()

        self.refresh_index()

        response = OfficerWorker().search('fu na')
        expect(response.hits.total).to.be.equal(1)


class UnitWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = UnitDocType(name='name')
        doc.save()

        self.refresh_index()

        response = UnitWorker().search('name')
        expect(response.hits.total).to.be.equal(1)


class NeighborhoodsWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = NeighborhoodsDocType(name='name')
        doc.save()

        self.refresh_index()

        response = NeighborhoodsWorker().search('name')
        expect(response.hits.total).to.be.equal(1)


class CommunityWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = CommunityDocType(name='name')
        doc.save()

        self.refresh_index()

        response = CommunityWorker().search('name')
        expect(response.hits.total).to.be.equal(1)


class CoAccusedOfficerWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = CoAccusedOfficerDocType(
            full_name='Kevin Osborn', co_accused_officer=[{
                'full_name': 'Cristiano Ronaldo',
                'badge': '123'
                }])
        doc.save()

        self.refresh_index()

        response = CoAccusedOfficerWorker().search('Cris')
        expect(response.hits.total).to.be.equal(1)
        co_accused_doc = response.hits[0]
        expect(co_accused_doc.full_name).to.eq('Kevin Osborn')
        expect(co_accused_doc.co_accused_officer[0]['full_name']).to.eq('Cristiano Ronaldo')


class UnitOfficerWorkerTestCase(IndexMixin, SimpleTestCase):
    def test_search(self):
        doc = UnitOfficerDocType(unit_name='001', full_name='Kevin Osborn', allegation_count=1)
        doc.save()
        doc = UnitOfficerDocType(unit_name='001', full_name='Kevin Cascone', allegation_count=0)
        doc.save()
        doc = UnitOfficerDocType(unit_name='002', full_name='Cristiano Cascone', allegation_count=0)
        doc.save()

        self.refresh_index()

        response = UnitOfficerWorker().search('001')
        expect(response.hits.total).to.be.equal(2)
        expect(response.hits[0].full_name).to.be.eq('Kevin Osborn')
        expect(response.hits[1].full_name).to.be.eq('Kevin Cascone')
