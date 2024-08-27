"""Test Create List API views."""

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from english.models import WordModel
from users.models import UserModel


class TestWordList(APITestCase):
    """Test word list api view."""

    words = [
        {'word_eng': 'red', 'word_rus': 'красный'},
        {'word_eng': 'white', 'word_rus': 'белый'},
        {'word_eng': 'green', 'word_rus': 'зеленый'},
        {'word_eng': 'blue', 'word_rus': 'синий'},
        {'word_eng': 'black', 'word_rus': 'черный'},
    ]

    def setUp(self) -> None:
        """Set up data."""
        self.owner = UserModel.objects.create_user(username='owner')
        self.user = UserModel.objects.create_user(username='user')
        for word in self.words:
            WordModel.objects.create(**word, user=self.owner)
        self.url = reverse('api-word')

    def test_get_word_list_by_owner(self) -> None:
        """Test list api view for owner."""
        client = APIClient()
        client.force_authenticate(user=self.owner)
        response = client.get(self.url)
        assert response.status_code == 200

    # def test_get_word_list_by_anonymous(self) -> None:
    #     """Test list api view for anonymous."""
    #     client = APIClient()
    #     response = client.get(self.url)
    #     assert response.status_code == 200

    def test_get_word_list_by_not_owner(self) -> None:
        """Test list api view for not owner."""
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(self.url)
        assert response.status_code == 200
