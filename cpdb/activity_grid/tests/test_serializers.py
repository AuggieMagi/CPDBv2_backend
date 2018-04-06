from django.test import SimpleTestCase

from robber import expect
from mock import Mock

from activity_grid.serializers import OfficerCardSerializer
from officers.doc_types import OfficerInfoDocType


class ActivityCardSerializerTestCase(SimpleTestCase):
    def test_serialize_officer_card(self):
        percentile_mock = Mock()
        percentile_mock.to_dict.return_value = {
            'id': 123,
            'year': 2016,
            'percentile_trr': '0.000',
            'percentile_allegation': '0.088',
            'percentile_allegation_civilian': '77.000',
            'percentile_allegation_internal': '0.020'
        }

        obj = Mock(
            id=123,
            full_name='Alex Mack',
            race='White',
            gender='Male',
            birth_year=1910,
            allegation_count=2,
            honorable_mention_count=1,
            sustained_count=1,
            discipline_count=1,
            civilian_compliment_count=0,
            percentiles=[percentile_mock]
        )

        expect(OfficerCardSerializer(obj).data).to.eq({
            'id': 123,
            'full_name': 'Alex Mack',
            'race': 'White',
            'gender': 'Male',
            'birth_year': 1910,
            'complaint_count': 2,
            'complaint_percentile': '0.088',
            'sustained_count': 1,
            'percentile': {
                'id': 123,
                'year': 2016,
                'percentile_trr': '0.000',
                'percentile_allegation': '0.088',
                'percentile_allegation_civilian': '77.000',
                'percentile_allegation_internal': '0.020'
            }
        })

    def test_serialize_officer_card_no_percentiles(self):
        obj = OfficerInfoDocType(
            id=123,
            full_name='Alex Mack',
            race='White',
            gender='Male',
            birth_year=1910,
            allegation_count=2,
            honorable_mention_count=1,
            sustained_count=1,
            discipline_count=1,
            civilian_compliment_count=0,
        )

        expect(OfficerCardSerializer(obj).data).to.eq({
            'id': 123,
            'full_name': 'Alex Mack',
            'race': 'White',
            'gender': 'Male',
            'birth_year': 1910,
            'complaint_count': 2,
            'complaint_percentile': None,
            'sustained_count': 1,
            'percentile': []
        })
