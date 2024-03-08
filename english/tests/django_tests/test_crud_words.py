from unittest import skip

from django.test import Client, TestCase
from django.urls import reverse

from contrib_app.contrib_test import flash_message_test
from english.models import WordModel
from users.models import UserModel

CREATE_WORD_PATH = 'english:words_create'
DELETE_WORD_PATH = 'english:words_delete'
DETAIL_WORD_PATH = 'english:words_detail'
UPDATE_WORD_PATH = 'english:words_update'
WORD_LIST_PATH = 'english:word_list'

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_CREATE_WORD_MSG = 'Слово добавлено'
SUCCESS_DELETE_WORD_MSG = 'Слово удалено'
SUCCESS_UPDATE_WORD_MSG = 'Слово изменено'


class TestCreateWordView(TestCase):
    """Test create word view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id,)
        self.another_user = UserModel.objects.get(id=another_user_id)
        self.create_data = {
            'words_eng': 'new word',
            'words_rus': 'новое слово',
            'word_count': 'CB',
        }
        self.url = reverse(CREATE_WORD_PATH)
        self.success_url = self.url

    def test_get_method_create_word_by_user(self):
        """Test create word by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_create_word_by_user(self):
        """Test create word by logged-in user, POST method page status 302."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.create_data)

        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_CREATE_WORD_MSG)
        assert WordModel.objects.filter(words_eng='new word').exists()

    def test_post_method_create_word_by_anonymous(self):
        """Test create word by anonymous, POST method page status 302."""
        response = self.client.post(self.url, self.create_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordModel.objects.filter(words_eng='new word').exists()

    def test_add_default_values(self):
        """Test add default user to word model."""
        self.client.force_login(self.user)
        self.client.post(self.url, self.create_data)
        added_word = WordModel.objects.get(words_eng='new word')
        assert added_word.user.username == self.user.username


class TestUpdateWordView(TestCase):
    """Test update word view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        user_id = 3
        user_word_id = 1
        another_user_id = 4
        self.user = UserModel.objects.get(pk=user_id)
        self.another_user = UserModel.objects.get(pk=another_user_id)
        self.update_data = {
            'words_eng': 'test',
            'words_rus': 'тест',
            'word_count': 'ST',
        }
        self.url = reverse(UPDATE_WORD_PATH, kwargs={'pk': user_word_id})
        self.success_url = reverse(WORD_LIST_PATH)

    def test_get_method_update_word_by_user(self):
        """Test update word by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_update_word_by_user(self):
        """Test update word by logged-in user, POST method page status 302."""
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_UPDATE_WORD_MSG)
        assert WordModel.objects.filter(words_eng='test').exists()

    def test_post_method_update_word_by_another_user(self):
        """Test update word by another user, POST method page status 302."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordModel.objects.filter(words_eng='test').exists()

    def test_post_method_update_word_by_anonymous(self):
        """Test update word by anonymous, POST method page status 302."""
        response = self.client.post(self.url, self.update_data)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert not WordModel.objects.filter(words_eng='test').exists()


class TestDeleteWordView(TestCase):
    """Test delete word view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

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
        """Test delete word by logged-in user, GET method page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_post_method_delete_word_by_user(self):
        """Test delete word by logged-in user, POST method page status 302."""
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, self.success_url, 302)
        flash_message_test(response, SUCCESS_DELETE_WORD_MSG)
        assert not WordModel.objects.filter(pk=self.word_id).exists()

    def test_post_method_delete_word_by_another_user(self):
        """Tes delete word by another user, POST method page status 302."""
        self.client.force_login(self.another_user)
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordModel.objects.filter(pk=self.word_id).exists()

    def test_post_method_delete_word_by_anonymous(self):
        """Test delete word by anonymous, POST method page status 302."""
        response = self.client.post(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
        assert WordModel.objects.filter(pk=self.word_id).exists()


class TestWordListView(TestCase):
    """Test word list view."""

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

    def setUp(self):
        """Set up data."""
        self.client: Client = Client()
        self.user_id = 3
        self.another_user_id = 4
        self.user = UserModel.objects.get(pk=self.user_id)
        self.another_user = UserModel.objects.get(pk=self.another_user_id)
        self.url = reverse(WORD_LIST_PATH)

    def test_show_word_list_to_specific_user(self):
        """Test display word list to specific user, page status 200."""
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        # assert by user id, that `words` contains only the user's words
        words = response.context["words"]
        user_ids = set(words.values_list('user', flat=True))
        self.assertTrue(*user_ids, self.user_id)

    def test_show_list_word_to_anonymous(self):
        """Test permission denied to display a word list for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

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

    fixtures = ['english/tests/fixtures/wse-fixtures-3.json']

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
        """Test permission denied to display a word for another user."""
        self.client.force_login(self.another_user)
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)

    def test_show_word_detail_to_anonymous(self):
        """Test permission denied to display a word for an anonymous."""
        response = self.client.get(self.url)
        self.assertRedirects(response, NO_PERMISSION_URL, 302)
        flash_message_test(response, NO_PERMISSION_MSG)
