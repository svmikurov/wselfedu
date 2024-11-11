"""Foreign word category CRUD tests."""

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


class CategoryTestData(TestData):
    """Foreign word category tests data."""

    fixtures = ['users', 'foreign']

    success_create_msg = 'Категория слов добавлена'
    success_update_msg = 'Категория слов изменена'
    success_delete_msg = 'Категория слов удалена'
    no_permission_msg = 'Для доступа необходимо войти в приложение'

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
            'foreign:categories_delete',
            kwargs={'pk': self.item_pk},
        )

        # Redirect urls.
        self.url_create_redirect = self.url_list
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class CategoryCreateTest(CreateTest, CategoryTestData):
    """Foreign word category create tests."""

    def test_create(self) -> None:
        """Add a test is exists category in the database."""
        super().test_create()
        assert self.manager.filter(name='category%').exists()

    def test_create_by_anonymous(self) -> None:
        """Add a test is no exists category in the database."""
        super().test_create_by_anonymous()
        assert not self.manager.filter(name='category%').exists()


class CategoryListTest(ListTest, CategoryTestData):
    """Foreign word category list tests."""


class CategoryUpdateTest(UpdateTest, CategoryTestData):
    """Foreign word category tests."""


class CategoryDeleteTest(DeleteTest, CategoryTestData):
    """Foreign word category delete tests."""


class CategoryDetailTest(DetailTest, CategoryTestData):
    """Foreign word category delete tests."""
