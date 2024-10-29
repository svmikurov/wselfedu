"""Foreign word CRUD tests."""

from unittest import skip

from django.db.models import F
from django.test import Client, TestCase
from django.urls import reverse

from config.constants import COMBINATION, ONE_WORD
from contrib.tests.crud import (
    CreateTest,
    DeleteTest,
    DetailTest,
    ListTest,
    TestData,
    UpdateTest,
)
from foreign.models import Word
from users.models import UserApp


class WordTestData(TestData):
    """Foreign word source tests data."""

    fixtures = ['users', 'foreign']

    success_create_msg = ''
    success_update_msg = 'Слово изменено'
    success_delete_msg = 'Слово удалено'
    no_permission_msg = 'Для доступа необходимо войти в приложение'

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 1
        self.manager = Word.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {
            'foreign_word': 'new word%',
            'native_word': 'новое слово',
            'word_count': COMBINATION,
        }

        # Users.
        self.owner_id = 3
        self.owner = UserApp.objects.get(pk=self.owner_id)
        self.not_owner = UserApp.objects.get(pk=4)

        # Urls.
        self.url_create = reverse('foreign:words_create')
        self.url_list = reverse('foreign:word_list')
        self.url_update = reverse(
            'foreign:words_update', kwargs={'pk': self.item_pk}
        )
        self.url_detail = reverse(
            'foreign:words_detail', kwargs={'pk': self.item_pk}
        )
        self.url_delete = reverse(
            'foreign:words_delete', kwargs={'pk': self.item_pk}
        )

        # Redirect urls.
        self.url_create_redirect = self.url_create
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class WordCreateTest(CreateTest, WordTestData):
    """Foreign word create tests."""

    def test_create(self) -> None:
        """Add a test for category existence."""
        super().test_create()
        assert self.manager.filter(foreign_word='new word%').exists()

    def test_create_by_anonymous(self) -> None:
        """Add a test for category not existence."""
        super().test_create_by_anonymous()
        assert not self.manager.filter(foreign_word='new word%').exists()


class WordListTest(ListTest, WordTestData):
    """Foreign word list tests."""


class WordUpdateTest(UpdateTest, WordTestData):
    """Foreign word update tests."""


class WordDeleteTest(DeleteTest, WordTestData):
    """Foreign word delete tests."""


class WordDetailTest(DetailTest, WordTestData):
    """Foreign word delete tests."""


class TestWordObjectList(TestCase):
    """Test to word list page object list."""

    fixtures = ['foreign', 'users']

    def setUp(self) -> None:
        """Set up data."""
        client: Client = Client()
        self.user_id = 3
        self.user = UserApp.objects.get(pk=self.user_id)
        url = reverse('foreign:word_list')

        client.force_login(self.user)
        self.response = client.get(url)
        self.object_list = self.response.context['object_list']
        self.html = self.response.content.decode()

    def test_context_object_name(self) -> None:
        """Test 'context_object_name'."""
        context_object_name = 'words'
        word_index_in_context = 0
        word_key = 'foreign_word'
        words = self.response.context[context_object_name].values()
        self.assertInHTML(words[word_index_in_context][word_key], self.html)

    def test_object_list_count(self) -> None:
        """Test to 'object_list' length of word list page."""
        user_word_count = Word.objects.filter(user=self.user).count()
        object_list_length = self.object_list.count()
        assert object_list_length == user_word_count

    def test_object_list_contains_category(self) -> None:
        """Test to 'object_list' word list page contains category."""
        category = 'category_u3_c2'
        categories = self.object_list.values_list('category__name', flat=True)
        assert category in categories

    def test_object_list_contains_source(self) -> None:
        """Test to 'object_list' word list page contains source."""
        source = 'source_u3_s1'
        sources = self.object_list.values_list('source__name', flat=True)
        assert source in sources

    def test_object_list_contains_word_count(self) -> None:
        """Test to 'object_list' word list page contains word count."""
        word_count = ONE_WORD
        readable_word_count = '<td>Слово</td>'
        counted = self.object_list.values_list('word_count', flat=True)
        assert word_count in counted
        self.assertInHTML(readable_word_count, self.html)

    def test_object_list_contains_assessment(self) -> None:
        """Test to 'object_list' word list page contains assessment."""
        assessment = 1
        assessments = self.object_list.values_list('assessment', flat=True)
        assert assessment in assessments

    def test_object_list_contains_favorite(self) -> None:
        """Test to 'object_list' word list page contains favorite."""
        favorite_word = ('word_u3_w3', True)
        another_word = ('word_u3_w7', False)
        words = self.object_list.values_list('foreign_word', 'favorites_anat')
        assert favorite_word in words
        assert another_word not in words


class WordListPageFilter(TestCase):
    """Test filters word at word list word page."""

    fixtures = ['tests/fixtures/foreign.json', 'tests/fixtures/users.json']

    def setUp(self) -> None:
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 3
        self.another_user_id = 4
        self.user = UserApp.objects.get(pk=self.user_id)
        self.another_user = UserApp.objects.get(pk=self.another_user_id)
        self.url = reverse('foreign:word_list')

    def test_contain_filter_only_user_choices(self) -> None:
        """Test filter contain only user item."""
        user_category = 'category_u3_c1'
        another_user_category = 'category_u4_c1'

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        html = response.content.decode()

        self.assertInHTML(user_category, html)
        self.assertNotIn(another_user_category, html)

    def test_checkbox_favorite_words(self) -> None:
        """Test checkbox favorites word."""
        self.client.force_login(self.user)
        response = self.client.get(self.url, {'only_favorite_words': True})

        objects_list = response.context['object_list']
        user_favorite_words = Word.objects.filter(
            wordfavorites__word=F('pk'),
            wordfavorites__user=self.user_id,
        )
        self.assertQuerySetEqual(
            objects_list,
            user_favorite_words.order_by('-foreign_word'),
        )

    def test_filter_word_list_by_word(self) -> None:
        """Test filtering the word list by text containing the word."""
        self.client.force_login(self.user)

        # filter by foreign word
        search_param = {'search_word': 'word_u3_w1'}
        response = self.client.get(self.url, search_param)
        self.assertContains(response, 'word_u3_w1', status_code=200)
        self.assertNotContains(response, 'word_u3_w2')

        # filter by native word
        search_param = {'search_word': 'слово_п3_с1'}
        response = self.client.get(self.url, search_param)
        self.assertContains(response, 'слово_п3_с1', status_code=200)
        self.assertNotContains(response, 'слово_п3_с2')

    @skip('Write a test')
    def test_filter_word_list_by_category(self) -> None:
        """Test filtering the word list by category."""

    @skip('Write a test')
    def test_filter_word_list_by_source(self) -> None:
        """Test filtering the word list by source."""

    @skip('Write a test')
    def test_filter_word_list_by_length(self) -> None:
        """Test filtering the word list by length."""
