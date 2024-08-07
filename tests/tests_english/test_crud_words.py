"""Test word CRUD module."""

from unittest import skip

from django.db.models import F
from django.test import Client, TestCase
from django.urls import reverse

from contrib.tests_extension import flash_message_test
from english.models import WordModel
from users.models import UserModel

CREATE_WORD_PATH = 'english:words_create'
DELETE_WORD_PATH = 'english:words_delete'
DETAIL_WORD_PATH = 'english:words_detail'
UPDATE_WORD_PATH = 'english:words_update'
WORD_LIST_PATH = 'english:word_list'

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_DELETE_WORD_MSG = 'Слово удалено'
SUCCESS_UPDATE_WORD_MSG = 'Слово изменено'


class TestCreateWordView(TestCase):
    """Test create word view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        another_user_id = 4
        self.user = UserModel.objects.get(
            pk=user_id,
        )
        self.another_user = UserModel.objects.get(id=another_user_id)
        self.create_data = {
            'word_eng': 'new word',
            'word_rus': 'новое слово',
            'word_count': 'CB',
        }
        self.url = reverse(CREATE_WORD_PATH)
        self.success_url = self.url

    def test_get_method_create_word_by_user(self):
        """Test create word by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    @skip('TODO: update message test, now JsonResponse')
    def test_post_method_create_word_by_user(self):
        """Test create word by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.create_data)

        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, 'Добавлено слово "new word"')
        assert WordModel.objects.filter(word_eng='new word').exists()

    def test_post_method_create_word_by_anonymous(self):
        """Test the permission to create a word for an anonymous."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordModel.objects.filter(word_eng='new word').exists()

    def test_add_default_values(self):
        """Test add default user to word model."""
        self.client.force_login(self.user)
        self.client.post(self.url, self.create_data)
        added_word = WordModel.objects.get(word_eng='new word')
        assert added_word.user.username == self.user.username


class TestUpdateWordView(TestCase):
    """Test update word view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_word_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.update_data = {
            'word_eng': 'test',
            'word_rus': 'тест',
            'word_count': 'ST',
        }
        self.url = reverse(UPDATE_WORD_PATH, kwargs={'pk': user_word_id})
        self.success_url = reverse(WORD_LIST_PATH)

    def test_get_method_update_word_by_user(self):
        """Test update word by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_word_by_user(self):
        """Test update word by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_UPDATE_WORD_MSG)
        assert WordModel.objects.filter(word_eng='test').exists()

    def test_post_method_update_word_by_another_user(self):
        """Test the permission to update a word for an anonymous."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordModel.objects.filter(word_eng='test').exists()

    def test_post_method_update_word_by_anonymous(self):
        """Test the permission to update a word for another user."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordModel.objects.filter(word_eng='test').exists()


class TestDeleteWordView(TestCase):
    """Test delete word view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        self.word_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(DELETE_WORD_PATH, kwargs={'pk': self.word_id})
        self.success_url = reverse(WORD_LIST_PATH)

    def test_get_method_delete_word_by_user(self):
        """Test delete word by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_delete_word_by_user(self):
        """Test delete word by logged-in user."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_DELETE_WORD_MSG)
        assert not WordModel.objects.filter(pk=self.word_id).exists()

    def test_post_method_delete_word_by_another_user(self):
        """Test the permission to delete a word for another user."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordModel.objects.filter(pk=self.word_id).exists()

    def test_post_method_delete_word_by_anonymous(self):
        """Test the permission to delete a word for an anonymous."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordModel.objects.filter(pk=self.word_id).exists()


class TestWordListView(TestCase):
    """Test word list view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 3
        self.another_user_id = 4
        self.user = UserModel.objects.get(pk=self.user_id)
        self.another_user = UserModel.objects.get(pk=self.another_user_id)
        self.url = reverse(WORD_LIST_PATH)

    def test_show_word_list_to_specific_user(self):
        """Test display word list to specific user."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # assert by user id, that `words` contains only the user's words
        words = response.context['words']
        user_ids = set(words.values_list('user', flat=True))
        self.assertTrue(*user_ids, self.user_id)

    def test_show_list_word_to_anonymous(self):
        """Test permission to display a word list for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)


class TestWordObjectList(TestCase):
    """Test to word list page object list."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        client: Client = Client()
        self.user_id = 3
        self.user = UserModel.objects.get(pk=self.user_id)
        url = reverse(WORD_LIST_PATH)

        client.force_login(self.user)
        self.response = client.get(url)
        self.object_list = self.response.context['object_list']
        self.html = self.response.content.decode()

    def test_context_object_name(self):
        """Test 'context_object_name'."""
        context_object_name = 'words'
        word_index_in_context = 0
        word_key = 'word_eng'
        words = self.response.context[context_object_name].values()
        self.assertInHTML(words[word_index_in_context][word_key], self.html)

    def test_object_list_count(self):
        """Test to 'object_list' length of word list page."""
        user_word_count = WordModel.objects.filter(user=self.user).count()
        object_list_length = self.object_list.count()
        assert object_list_length == user_word_count

    def test_object_list_contains_category(self):
        """Test to 'object_list' word list page contains category."""
        category = 'category_u3_c2'
        categories = self.object_list.values_list('category__name', flat=True)
        assert category in categories

    def test_object_list_contains_source(self):
        """Test to 'object_list' word list page contains source."""
        source = 'source_u3_s1'
        sources = self.object_list.values_list('source__name', flat=True)
        assert source in sources

    def test_object_list_contains_word_count(self):
        """Test to 'object_list' word list page contains word count."""
        word_count = 'OW'
        readable_word_count = '<td>Слово</td>'
        counted = self.object_list.values_list('word_count', flat=True)
        assert word_count in counted
        self.assertInHTML(readable_word_count, self.html)

    def test_object_list_contains_assessment(self):
        """Test to 'object_list' word list page contains assessment."""
        assessment = 1
        assessments = self.object_list.values_list('assessment', flat=True)
        assert assessment in assessments

    def test_object_list_contains_favorite(self):
        """Test to 'object_list' word list page contains favorite."""
        favorite_word = ('word_u3_w3', True)
        another_word = ('word_u3_w7', False)
        words = self.object_list.values_list('word_eng', 'favorites_anat')
        assert favorite_word in words
        assert another_word not in words


class WordListPageFilter(TestCase):
    """Test filters word at word list word page."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 3
        self.another_user_id = 4
        self.user = UserModel.objects.get(pk=self.user_id)
        self.another_user = UserModel.objects.get(pk=self.another_user_id)
        self.url = reverse(WORD_LIST_PATH)

    def test_contain_filter_only_user_choices(self):
        """Test filter contain only user item."""
        user_category = 'category_u3_c1'
        another_user_category = 'category_u4_c1'

        self.client.force_login(self.user)
        response = self.client.get(self.url)
        html = response.content.decode()

        self.assertInHTML(user_category, html)
        self.assertNotIn(another_user_category, html)

    def test_checkbox_favorite_words(self):
        """Test checkbox favorites word."""
        self.client.force_login(self.user)
        response = self.client.get(self.url, {'only_favorite_words': True})

        objects_list = response.context['object_list']
        user_favorite_words = WordModel.objects.filter(
            wordsfavoritesmodel__word=F('pk'),
            wordsfavoritesmodel__user=self.user_id,
        )
        self.assertQuerySetEqual(objects_list, user_favorite_words)

    def test_filter_word_list_by_word(self):
        """Test filtering the word list by text containing the word."""
        self.client.force_login(self.user)

        # filter by english word
        search_param = {'search_word': 'word_u3_w1'}
        response = self.client.get(self.url, search_param)
        self.assertContains(response, 'word_u3_w1', status_code=200)
        self.assertNotContains(response, 'word_u3_w2')

        # filter by russian word
        search_param = {'search_word': 'слово_п3_с1'}
        response = self.client.get(self.url, search_param)
        self.assertContains(response, 'слово_п3_с1', status_code=200)
        self.assertNotContains(response, 'слово_п3_с2')

    @skip('Write a test')
    def test_filter_word_list_by_category(self):
        """Test filtering the word list by category."""

    @skip('Write a test')
    def test_filter_word_list_by_source(self):
        """Test filtering the word list by source."""

    @skip('Write a test')
    def test_filter_word_list_by_length(self):
        """Test filtering the word list by length."""


class TestWordDetailView(TestCase):
    """Test word detail view."""

    fixtures = ['tests/tests_english/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_word_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.url = reverse(DETAIL_WORD_PATH, kwargs={'pk': user_word_id})

    def test_show_word_detail_to_user(self):
        """Test show word detail to user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_show_word_for_another_user(self):
        """Test the permission to display a word for another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_word_detail_to_anonymous(self):
        """Test the permission to display a word for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
