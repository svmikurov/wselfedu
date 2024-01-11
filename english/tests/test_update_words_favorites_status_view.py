"""
For now:
    - can update: admin, auth user;
    - can't update: not auth user.

Fixtures are created and taken from the db-wse-fixtures.sqlite3, contain:
    user.pk=1 is admin
    user.pk=2 is user1
"""
from django.test import TestCase
from django.urls import reverse_lazy

from english.models import WordModel
from english.models import WordsFavoritesModel
from users.models import UserModel


class TestUpdateWordsFavoritesStatusView(TestCase):
    """Тест обновления значения оценка пользователем уровня знания слова."""

    fixtures = ['english/tests/fixtures/wse-fixtures.json']

    def setUp(self):
        self.user = UserModel.objects.get(pk=2)
        self.word_id = WordModel.objects.get(pk=1).pk
        self.current_status = WordsFavoritesModel.objects.filter(
            user=self.user,
            word=self.word_id,
        )
        print(f'self.current_status = {self.current_status}')
        self.url = reverse_lazy(
            'eng:words_favorites_view',
            kwargs={'word_id': self.word_id},
        )
        kwargs = {'task_status': 'question'}
        self.success_url = reverse_lazy('eng:repetition', kwargs=kwargs)
        self.post_data = {'favorites_action': 'add'}

    def test_update_bu_auth_user(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, self.post_data)
        self.current_status = WordsFavoritesModel.objects.filter(
            user=self.user,
            word=self.word_id,
        )
        print(f'self.current_status = {self.current_status}')
        self.assertRedirects(response, self.success_url, 302)
