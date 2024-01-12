from django.test import TestCase

from english.models import WordModel
from english.services import include_favorites_to_words_qs


class TestJoinQS(TestCase):

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user_id = 1
        self.words_objects = WordModel.objects
        self.expected_queryset = [
            {
                'pk': 2,
                'words_eng': 'word02',
                'words_rus': 'слово02',
                'source': 2,
                'assessment': 3,
                'created_at': '2024-01-11T15:00:49Z',
            },
            {
                'pk': 3,
                'words_eng': 'word03',
                'words_rus': 'слово03',
                'source': 2,
                'assessment': 7,
                'created_at': '2024-01-12T15:12:31Z',
            },
            {
                'pk': 4,
                'words_eng': 'word04',
                'words_rus': 'слово04',
                'source': 2,
                'assessment': 9,
                'created_at': '2024-01-12T15:13:06Z',
            },
        ]

    def test(self):
        current_queryset = include_favorites_to_words_qs(
            self.words_objects,
            self.user_id,
        )
        for index, query in enumerate(current_queryset):
            for field in query:
                print(f'from test: field = {field}')
                print(f'from test: index = {index}')
                print(f'from test: query.get(field) = {query.get(field)}')
                print(f'from test: self.expected_queryset[index].get(field) = {self.expected_queryset[index].get(field)}')
                assert query.get(field) == self.expected_queryset[index].get(field)
