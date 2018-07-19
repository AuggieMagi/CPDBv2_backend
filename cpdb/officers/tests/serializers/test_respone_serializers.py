from datetime import datetime

from django.test import SimpleTestCase
from mock import Mock
from robber import expect

from officers.serializers.respone_serialiers import NewTimelineSerializer, OfficerMobileSerializer


class NewTimelineSerializerTestCase(SimpleTestCase):
    def test_serialization(self):
        obj = Mock()
        obj.to_dict = Mock(return_value={
            'a': 'b',
            'c': 'd',
            'date_sort': datetime.now(),
            'priority_sort': 40,
            'officer_id': 123

        })
        expect(NewTimelineSerializer(obj).data).to.eq({
            'a': 'b',
            'c': 'd'
        })

    def test_serialize_multiple(self):
        obj1 = Mock()
        obj1.to_dict = Mock(return_value={
            'a': 'b',
            'date_sort': datetime.now(),
            'priority_sort': 40,
            'officer_id': 123
        })
        obj2 = Mock()
        obj2.to_dict = Mock(return_value={
            'c': 'd',
            'date_sort': datetime.now(),
            'priority_sort': 40,
            'officer_id': 456
        })
        expect(NewTimelineSerializer([obj1, obj2], many=True).data).to.eq([
            {'a': 'b'},
            {'c': 'd'}
        ])


class OfficerMobileSerializerTestCase(SimpleTestCase):
    def test_serialization(self):
        obj = Mock(**{
            'id': 789,
            'last_unit': Mock(id=1, unit_name='', description=''),
            'date_of_appt': '01-01-2010',
            'date_of_resignation': '01-01-2015',
            'active': True,
            'rank': '',
            'full_name': 'Full Name',
            'race': 'Asian',
            'badge': '789',
            'historic_badges': ['123', '456'],
            'unit': Mock(**{
                'id': 1,
                'unit_name': '1',
                'description': 'Unit 1'
            }),
            'gender': 'Male',
            'birth_year': 1950,
            'allegation_count': 2,
            'complaint_percentile': 32.5,
            'honorable_mention_count': 1,
            'sustained_count': 1,
            'discipline_count': 1,
            'civilian_compliment_count': 6,
            'honorable_mention_percentile': 0.99,
            'trr_count': 1,
            'major_award_count': 1,
            'current_salary': 90000,
            'percentiles': [
                Mock(**{
                    'percentile_allegation': 99.345,
                    'percentile_trr': 0.000,
                    'year': 2001,
                    'id': 1,
                    'percentile_allegation_civilian': 98.434,
                    'percentile_allegation_internal': 99.784,
                }),
                Mock(**{
                    'percentile_allegation': 99.345,
                    'percentile_trr': 0.000,
                    'year': 2002,
                    'id': 1,
                    'percentile_allegation_civilian': 98.434,
                    'percentile_allegation_internal': 99.784,
                }),
            ],
        })
        expect(OfficerMobileSerializer(obj).data).to.eq({
            'officer_id': 789,
            'full_name': 'Full Name',
            'percentiles': [
                {
                    'percentile_allegation': '99.345',
                    'percentile_trr': '0.000',
                    'year': 2001,
                    'id': 1,
                    'percentile_allegation_civilian': '98.434',
                    'percentile_allegation_internal': '99.784',
                },
                {
                    'percentile_allegation': '99.345',
                    'percentile_trr': '0.000',
                    'year': 2002,
                    'id': 1,
                    'percentile_allegation_civilian': '98.434',
                    'percentile_allegation_internal': '99.784',
                },
            ],
            'unit': {
                'unit_id': 1,
                'unit_name': '1',
                'description': 'Unit 1'
            },
            'date_of_appt': '01-01-2010',
            'date_of_resignation': '01-01-2015',
            'active': True,
            'rank': '',
            'race': 'Asian',
            'badge': '789',
            'birth_year': 1950,
            'historic_badges': ['123', '456'],
            'gender': 'Male',
            'allegation_count': 2,
            'complaint_percentile': 32.5,
            'honorable_mention_count': 1,
            'sustained_count': 1,
            'discipline_count': 1,
            'civilian_compliment_count': 6,
            'trr_count': 1,
            'major_award_count': 1,
            'honorable_mention_percentile': 0.99,
        })

    def test_serialization_missing_data(self):
        data_dict = {
            'id': 789,
            'active': True,
            'rank': '',
            'full_name': 'Full Name',
            'race': 'Asian',
            'gender': 'Male',
        }
        obj = Mock(spec=data_dict.keys(), **data_dict)
        expected_response = {
            'officer_id': 789,
            'full_name': 'Full Name',
            'active': True,
            'rank': '',
            'race': 'Asian',
            'gender': 'Male',
        }
        expect(OfficerMobileSerializer(obj).data).to.eq(expected_response)