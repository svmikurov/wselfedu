"""Test CRUD request Term category.

Each user has their own categories.
"""

from http import HTTPStatus

import pytest
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from glossary.models import TermCategory
from users.models import UserApp

pytest.skip(
    '"/category/" URL path is temporarily unused',
    allow_module_level=True,
)


class SetUpTest(APITestCase):
    """Setup of CRUD Term tests."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        """Set up the test."""
        self.api_client = APIClient()
        self.url = reverse('glossary_rest:category')
        self.user2 = UserApp.objects.get(pk=2)
        self.user3 = UserApp.objects.get(pk=3)
        TermCategory.objects.create(name='cat2-1', user=self.user2)
        TermCategory.objects.create(name='cat2-2', user=self.user2)
        TermCategory.objects.create(name='cat3', user=self.user3)
        self.category_name = 'cat2-2'


class TestListGlossaryCategory(SetUpTest):
    """Test list of Term category."""

    def test_auth_request(self) -> None:
        """Test request glossary categories by auth user."""
        self.api_client.force_authenticate(self.user2)
        response = self.api_client.get(self.url)
        categories = response.json()['results']

        assert response.status_code == HTTPStatus.OK
        # User has 2 categories
        assert len(categories) == 2
        assert categories.pop()['humanly'] == self.category_name

    def test_anonymous_request(self) -> None:
        """Test request glossary categories by anonymous."""
        response = self.api_client.get(self.url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class TestCreateGlossaryCategory(SetUpTest):
    """Test create Term category."""

    def test_create_category_by_auth_user(self) -> None:
        """Test create category by auth user."""
        self.api_client.force_authenticate(self.user2)
        payload = {'humanly': 'cat1'}
        response = self.api_client.post(self.url, payload, format='json')

        assert response.status_code == HTTPStatus.CREATED

    def test_create_category_by_anonymous(self) -> None:
        """Test create category by anonymous."""
        payload = {'humanly': 'cat1'}
        response = self.api_client.post(self.url, payload, format='json')

        assert response.status_code == HTTPStatus.UNAUTHORIZED


class RetrieveGlossaryCategoryTest(SetUpTest):
    """Test retrieve Term category."""

    def setUp(self) -> None:
        """Set up retrieve."""
        super().setUp()
        self.category = TermCategory.objects.get(name=self.category_name)
        self.url = self.url + f'{self.category.pk}/'

    def test_retrieve_category_by_owner(self) -> None:
        """Test retrieve category by owner."""
        self.api_client.force_authenticate(self.user2)
        response = self.api_client.get(self.url)

        assert response.status_code == HTTPStatus.OK
        assert response.json()['humanly'] == self.category_name

    def test_retrieve_category_anonymous(self) -> None:
        """Test retrieve category anonymous."""
        response = self.api_client.get(self.url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_retrieve_category_by_another_user(self) -> None:
        """Test retrieve category by another user."""
        self.api_client.force_authenticate(self.user3)
        response = self.api_client.get(self.url)

        assert response.status_code == HTTPStatus.FORBIDDEN


class DeleteGlossaryCategoryTest(SetUpTest):
    """Test delete Term category."""

    def setUp(self) -> None:
        """Set up delete."""
        super().setUp()
        self.category = TermCategory.objects.get(name=self.category_name)
        self.url = self.url + f'{self.category.pk}/'

    def test_delete_by_owner(self) -> None:
        """Test delete category by owner."""
        self.api_client.force_authenticate(self.user2)
        response = self.api_client.delete(self.url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not TermCategory.objects.filter(pk=self.category.pk).exists()  # noqa: E501

    def test_delete_another_user(self) -> None:
        """Test delete category by another user."""
        self.api_client.force_authenticate(self.user3)
        response = self.api_client.delete(self.url)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert TermCategory.objects.filter(pk=self.category.pk).exists()

    def test_delete_anonymous(self) -> None:
        """Test delete category by anonymous."""
        response = self.api_client.delete(self.url)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert TermCategory.objects.filter(pk=self.category.pk).exists()


class UpdateGlossaryCategoryTest(SetUpTest):
    """Test update Term category."""

    def setUp(self) -> None:
        """Set up update."""
        super().setUp()
        self.category = TermCategory.objects.get(name=self.category_name)
        self.url = self.url + f'{self.category.pk}/'
        self.to_update = {'humanly': 'update'}

    def test_update_by_owner(self) -> None:
        """Test update category by owner."""
        self.api_client.force_authenticate(self.user2)
        response = self.api_client.put(self.url, data=self.to_update)
        category = TermCategory.objects.get(pk=self.category.pk)

        assert response.status_code == HTTPStatus.OK
        assert category.name == self.to_update['humanly']

    def test_update_another_user(self) -> None:
        """Test update category by another user."""
        self.api_client.force_authenticate(self.user3)
        response = self.api_client.put(self.url, data=self.to_update)
        category = TermCategory.objects.get(pk=self.category.pk)

        assert response.status_code == HTTPStatus.FORBIDDEN
        assert category.name != self.to_update['humanly']

    def test_update_anonymous(self) -> None:
        """Test update category by anonymous."""
        response = self.api_client.put(self.url, data=self.to_update)
        category = TermCategory.objects.get(pk=self.category.pk)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert category.name != self.to_update['humanly']
