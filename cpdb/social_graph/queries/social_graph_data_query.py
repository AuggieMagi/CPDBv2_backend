import functools
from django.db import connection

from social_graph.serializers import OfficerSerializer, AccusedSerializer
from data.models import Officer, Allegation
from utils.raw_query_utils import dict_fetch_all


DEFAULT_THRESHOLD = 2
COMPLAINT_ORIGIN_FILTER_MAPPING = {
    'OFFICER': 'AND data_allegation.is_officer_complaint IS TRUE',
    'CIVILIAN': 'AND data_allegation.is_officer_complaint IS FALSE',
}
DEFAULT_COMPLAINT_ORIGIN = 'CIVILIAN'


class SocialGraphDataQuery(object):
    def __init__(
        self,
        officers,
        threshold=DEFAULT_THRESHOLD,
        complaint_origin=DEFAULT_COMPLAINT_ORIGIN,
        show_connected_officers=False,
    ):
        self.officers = officers
        self.threshold = threshold if threshold else DEFAULT_THRESHOLD
        self.complaint_origin = complaint_origin if complaint_origin is not None else DEFAULT_COMPLAINT_ORIGIN
        self.show_connected_officers = show_connected_officers

    def _officer_allegation_query(self, select_fields):
        officer_ids_string = ", ".join([str(officer.id) for officer in self.officers])
        return f"""
            SELECT {select_fields}
            FROM data_officerallegation AS A
            INNER JOIN data_officerallegation AS B ON A.allegation_id = B.allegation_id
            LEFT JOIN data_allegation ON data_allegation.crid = A.allegation_id
            WHERE A.officer_id < B.officer_id
            AND (
                B.officer_id IN ({officer_ids_string})
                {'OR' if self.show_connected_officers else 'AND'} A.officer_id IN ({officer_ids_string})
            )
            AND data_allegation.incident_date IS NOT NULL
            {COMPLAINT_ORIGIN_FILTER_MAPPING.get(self.complaint_origin, '')}
        """

    def _coaccused_data_query(self):
        officer_allegation_query = self._officer_allegation_query(f"""
            A.officer_id AS officer_id_1,
            B.officer_id AS officer_id_2,
            A.allegation_id AS allegation_id,
            data_allegation.incident_date AS incident_date,
            ROW_NUMBER() OVER (PARTITION BY A.officer_id, B.officer_id ORDER BY incident_date) AS accussed_count
        """)
        return f"""
            SELECT * FROM ({officer_allegation_query}) coaccused_data WHERE accussed_count >= {self.threshold}
            ORDER BY incident_date
        """

    def _allegation_id_query(self):
        officer_allegation_query = self._officer_allegation_query(f"""
           A.officer_id AS officer_id_1,
           B.officer_id AS officer_id_2,
           A.allegation_id AS allegation_id,
           COUNT(*) OVER (PARTITION BY A.officer_id, B.officer_id) AS total_accussed_count
        """)
        return f"""
            SELECT allegation_id FROM ({officer_allegation_query}) coaccused_data
            WHERE total_accussed_count >= {self.threshold}
        """

    @property
    @functools.lru_cache()
    def coaccused_data(self):
        if self.officers:
            with connection.cursor() as cursor:
                cursor.execute(self._coaccused_data_query())
                return dict_fetch_all(cursor)
        else:
            return []

    @property
    @functools.lru_cache()
    def allegation_ids(self):
        if self.officers:
            with connection.cursor() as cursor:
                cursor.execute(self._allegation_id_query())
                return [row['allegation_id'] for row in dict_fetch_all(cursor)]
        else:
            return []

    def list_event(self, static=False):
        events = list({row['incident_date'].date().strftime('%Y-%m-%d') for row in self.coaccused_data})
        events.sort()
        return [events[-1]] if static else events

    def all_officers(self):
        if self.show_connected_officers:
            officer_ids = [row['officer_id_1'] for row in self.coaccused_data]
            officer_ids += [row['officer_id_2'] for row in self.coaccused_data]
            officer_ids += [officer.id for officer in self.officers]
            officer_ids = list(set(officer_ids))
            return Officer.objects.filter(id__in=officer_ids).order_by('first_name', 'last_name')
        else:
            return self.officers.order_by('first_name', 'last_name')

    def graph_data(self, static=False):
        if self.officers:
            return {
                'coaccused_data': AccusedSerializer(self.coaccused_data, many=True).data,
                'officers': OfficerSerializer(self.all_officers(), many=True).data,
                'list_event': self.list_event(static)
            }
        else:
            return {}

    def allegations(self):
        return Allegation.objects.filter(crid__in=self.allegation_ids).order_by('incident_date')
