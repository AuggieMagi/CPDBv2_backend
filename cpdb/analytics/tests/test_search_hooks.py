from django.test import TestCase

from robber import expect

from analytics.search_hooks import QueryTrackingSearchHook
from analytics.models import SearchTracking
from analytics.factories import SearchTrackingFactory


class QueryTrackingSearchHookTestCase(TestCase):
    def test_execute_create(self):
        QueryTrackingSearchHook.execute(term='query', results={})
        expect(SearchTracking.objects.count()).to.be.eq(1)
        expect(SearchTracking.objects.first().query).to.be.eq('query')

    def test_execute_update(self):
        SearchTrackingFactory(query='query', results=10, usages=5)
        QueryTrackingSearchHook.execute(term='query', results={'officer': [{}, {}], 'coaccused': [{}, {}]})
        expect(SearchTracking.objects.count()).to.be.eq(1)
        search_tracking = SearchTracking.objects.first()
        expect(search_tracking.query).to.be.eq('query')
        expect(search_tracking.usages).to.be.eq(6)
        expect(search_tracking.results).to.be.eq(4)
