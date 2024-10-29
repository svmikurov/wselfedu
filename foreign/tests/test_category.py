"""Foreign word CRUD tests."""

from django.test import Client
from django.urls import reverse

from contrib.tests.crud import (
    CreateTest,
    DeleteTest,
    DetailTest,
    ListTest,
    TestData,
    UpdateTest,
)
from foreign.models import WordCategory
from users.models import UserApp

NO_PERMISSION_MSG = 'Для доступа необходимо войти в приложение'
NO_PERMISSION_URL = reverse('users:login')

SUCCESS_CREATE_CATEGORY_MSG = 'Категория слов добавлена'
SUCCESS_UPDATE_CATEGORY_MSG = 'Категория слов изменена'
SUCCESS_DELETE_CATEGORY_MSG = 'Категория слов удалена'


class CategoryTestData(TestData):
    """Foreign word source tests data."""

    fixtures = ['users', 'foreign']

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 1
        self.manager = WordCategory.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {
            'name': 'category%',
        }

        # Users.
        self.owner_id = 3
        self.owner = UserApp.objects.get(pk=self.owner_id)
        self.not_owner = UserApp.objects.get(pk=2)

        # Urls.
        self.url_create = reverse('foreign:categories_create')
        self.url_list = reverse('foreign:category_list')
        self.url_update = reverse(
            'foreign:categories_update', kwargs={'pk': self.item_pk}
        )
        self.url_detail = reverse(
            'foreign:categories_detail', kwargs={'pk': self.item_pk}
        )
        self.url_delete = reverse(
            'foreign:categories_delete', kwargs={'pk': self.item_pk}
        )

        # Redirect urls.
        self.url_create_redirect = self.url_list
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class CategoryCreateTest(CreateTest, CategoryTestData):
    """Foreign word source create tests."""

    def test_create(self) -> None:
        """Add exists category tests."""
        super().test_create()
        assert self.manager.filter(name='category%').exists()

    def test_create_by_anonymous(self) -> None:
        """Add not exists category tests."""
        super().test_create_by_anonymous()
        assert not self.manager.filter(name='category%').exists()


class CategoryListTest(ListTest, CategoryTestData):
    """Foreign word source list tests."""


class CategoryUpdateTest(UpdateTest, CategoryTestData):
    """Foreign word update tests."""


class CategoryDeleteTest(DeleteTest, CategoryTestData):
    """Foreign word source delete tests."""


class CategoryDetailTest(DetailTest, CategoryTestData):
    """Foreign word source delete tests."""
