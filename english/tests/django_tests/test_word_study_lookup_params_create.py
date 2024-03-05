import datetime

from django.utils import timezone

from django.test import TestCase

from english.models import WordModel
from english.services import create_lookup_params


class TestCreateLookupParams(TestCase):

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user_id = 2
        self.querydict = {
            'favorites': True, 'category': 0, 'source': 0,
            'period_start_date': 'NC', 'period_end_date': 'DT',
            'word_count': ['OW', 'CB', 'NC'],
            'knowledge_assessment': ['L', 'E'],
        }
        self.begin_date_period = (
            WordModel.objects.order_by('updated_at').first().updated_at
        )
        # В word_count__in программно добавляется 'NC'.
        self.params = {
            'favorites__pk': 2,
            'word_count__in': ['OW', 'CB', 'NC'],
            'created_at__range': (
                self.begin_date_period.strftime(
                    '%Y-%m-%d 00:00:00+00:00'),
                datetime.datetime.now(tz=timezone.utc).strftime(
                    '%Y-%m-%d 23:59:59+00:00'),
            ),
            'worduserknowledgerelation__knowledge_assessment__in': [
                0, 1, 2, 3, 4, 5, 6, 9, 10
            ],
        }

    def test_create_lookup_parameters(self):
        """Тест получения из request и переименования параметров поиска в БД.
        """
        params = create_lookup_params(self.querydict, self.user_id)
        self.assertEqual(self.params, params)
