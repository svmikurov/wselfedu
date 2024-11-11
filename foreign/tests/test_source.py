"""Foreign word source CRUD tests."""

from django.test import Client
from django.urls import reverse

from contrib.tests.crud import (
    CreateTest,
    DeleteProtectTest,
    DetailTest,
    ListTest,
    TestData,
    UpdateTest,
)
from foreign.models import WordSource
from users.models import UserApp


class SourceTestData(TestData):
    """Foreign word source tests data."""

    fixtures = ['users', 'foreign']

    success_create_msg = 'Источник слов добавлен'
    success_update_msg = 'Источник слов изменен'
    success_delete_msg = 'Источник слов удален'
    no_permission_msg = 'Для доступа необходимо войти в приложение'
    delete_protected_msg = (
        'Невозможно удалить этот объект, так как он '
        'используется в другом месте приложения'
    )

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

        # Items.
        self.item_pk = 2
        self.item_pk_delete_protected = 1
        self.manager = WordSource.objects
        self.item = self.manager.get(pk=self.item_pk)
        self.item_data = {'name': 'new source%'}

        # Users.
        self.owner_id = 3
        self.owner = UserApp.objects.get(pk=self.owner_id)
        self.not_owner = UserApp.objects.get(pk=2)

        # Urls.
        self.url_create = reverse('foreign:source_create')
        self.url_list = reverse('foreign:source_list')
        self.url_update = reverse(
            'foreign:source_update', kwargs={'pk': self.item_pk}
        )
        self.url_detail = reverse(
            'foreign:source_detail', kwargs={'pk': self.item_pk}
        )
        self.url_delete = reverse(
            'foreign:source_delete', kwargs={'pk': self.item_pk}
        )
        self.url_delete_protected = reverse(
            'foreign:source_delete',
            kwargs={'pk': self.item_pk_delete_protected},
        )

        # Redirect urls.
        self.url_create_redirect = self.url_list
        self.url_update_redirect = self.url_list
        self.url_delete_redirect = self.url_list
        self.url_delete_protected_redirect = self.url_list
        self.url_not_owner_redirect = reverse('users:login')


class SourceCreateTest(CreateTest, SourceTestData):
    """Foreign word source create tests."""

    def test_create(self) -> None:
        """Add a test is exists source in the database."""
        super().test_create()
        assert self.manager.filter(name='new source%').exists()

    def test_create_by_anonymous(self) -> None:
        """Add a test is no exists source in the database."""
        super().test_create_by_anonymous()
        assert not self.manager.filter(name='new source%').exists()


class SourceListTest(ListTest, SourceTestData):
    """Foreign word source list tests."""


class SourceUpdateTest(UpdateTest, SourceTestData):
    """Foreign word source tests."""


class SourceDeleteTest(DeleteProtectTest, SourceTestData):
    """Foreign word source delete tests."""


class SourceDetailTest(DetailTest, SourceTestData):
    """Foreign word source delete tests."""
