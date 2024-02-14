from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse_lazy

from english.views import WordListView


class TestWordListView(TestCase):

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.url = reverse_lazy('english:word_list')

    def test_status_words_list_page(self):
        """Тест статус 200 страницы списка слов."""
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        response = WordListView.as_view()(request)
        self.assertTrue(response.status_code, 200)

    def test_search_word(self):
        """Тест фильтра списка по слову."""
        # filter by english
        search_parameter = {'search_word': 'word02'}
        response = self.client.get(self.url, search_parameter)
        self.assertContains(response, 'word02')
        self.assertNotContains(response, 'word01')

        # filter by russian
        search_parameter = {'search_word': 'слово01'}
        response = self.client.get(self.url, search_parameter)
        self.assertContains(response, 'слово01')
        self.assertNotContains(response, 'слово02')
