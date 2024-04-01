from django.test import Client, TestCase

from english.services import get_words_for_study


class TestGetWordFordStudy(TestCase):
    """Test get word for study.

    self.lookup_params : dict
        Where:
            dict key - lookup method (e.g. `category_id` or `word_count__in`);
            dict value - lookup criterion (e.g. `2` or `['OW', 'CB', 'NC']`).
        `favorites__pk` :  int
            If the key is present and has a value equal to the user ID, then
            the word is considered favorite by this user
        `word_count__in` : list[str]
            May contain a combination of values:
                `OW` - own word,
                `CB` - combination of words,
                `PS` - part of a sentence,
                `ST` - sentence.
        'worduserknowledgerelation__knowledge_assessment__in' : list[int]
            May contain a combination of values:
                `[0, 1, 2, 3, 4, 5, 6]` - word study;
                `[7, 8,]` - word repetition;
                `[9, 10]` - word examination;
                `[11]` - word knowledge.
    """

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        self.client = Client()
        self.user_id = 3

        self.lookup_params = {
            # 'favorites__pk': ...,
            # 'category_id': ...,
            # 'source_id': ...,
            # 'created_at__range': ...,
            # 'word_count__in': ['OW', 'CB'],
            'worduserknowledgerelation__knowledge_assessment__in': [*range(9)]
        }

    def test_get_only_user_words(self):
        """Test get only user words."""
        lookup_params = {
            'worduserknowledgerelation__knowledge_assessment__in': [*range(12)]
        }
        words = get_words_for_study(
            lookup_params, self.user_id
        ).values_list('user', flat=True)
        self.assertEqual(*set(words), self.user_id)
