from officers.index_aliases import officers_index_alias
from officers.indexers import (
    OfficersIndexer, CRTimelineEventIndexer, UnitChangeTimelineEventIndexer,
    JoinedTimelineEventIndexer, SocialGraphIndexer, OfficerMetricsIndexer,
    OfficerPercentileIndexer
)


class OfficerSummaryTestCaseMixin(object):
    def setUp(self):
        officers_index_alias.write_index.delete(ignore=404)
        officers_index_alias.read_index.create(ignore=400)

    def refresh_index(self):
        with officers_index_alias.indexing():
            OfficersIndexer().reindex()
            OfficerMetricsIndexer().reindex()
            CRTimelineEventIndexer().reindex()
            UnitChangeTimelineEventIndexer().reindex()
            JoinedTimelineEventIndexer().reindex()
            SocialGraphIndexer().reindex()
            OfficerPercentileIndexer().reindex()

        officers_index_alias.write_index.refresh()
