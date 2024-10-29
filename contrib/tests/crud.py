"""CRUD test mixins."""

from http import HTTPStatus

from django.db.models.manager import Manager
from django.forms import model_to_dict
from django.test import Client

from users.models import UserApp


class TestMixinAnnotations:
    """Test mixins annotations."""

    client: Client
    owner: UserApp
    not_owner: UserApp
    manager: Manager
    item_pk: int
    item_data: dict
    url_create: str
    url_list: str
    url_update: str
    url_delete: str
    url_create_redirect: str
    url_update_redirect: str
    url_delete_redirect: str
    url_not_owner_redirect: str


class CreateTestMixin(TestMixinAnnotations):
    """Create tests mixin."""

    def test_create_get_method(self) -> None:
        """Test the item create, get method."""
        self.client.force_login(self.owner)
        response = self.client.get(self.url_create)
        assert response.status_code == HTTPStatus.OK

    def test_create(self) -> None:
        """Test the item create."""
        self.client.force_login(self.owner)
        response = self.client.post(self.url_create, self.item_data)
        self.assertRedirects(
            response, self.url_create_redirect, HTTPStatus.FOUND
        )


class ListTestMixin(TestMixinAnnotations):
    """List tests mixin."""

    def test_list(self) -> None:
        """Test the item list."""
        self.client.force_login(self.owner)
        response = self.client.get(self.url_list)
        assert response.status_code == HTTPStatus.OK

    def test_list_anonymous(self) -> None:
        """Test the item list, for anonymous."""
        response = self.client.get(self.url_list)
        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )


class UpdateTestMixin(TestMixinAnnotations):
    """Update tests mixin."""

    def test_update_get_method(self) -> None:
        """Test the item update, get method."""
        self.client.force_login(self.owner)
        response = self.client.get(self.url_update)
        assert response.status_code == HTTPStatus.OK

    def test_update(self) -> None:
        """Test the item update."""
        self.client.force_login(self.owner)
        response = self.client.post(self.url_update, self.item_data)
        item = self.manager.get(pk=self.item_pk)

        self.assertRedirects(
            response, self.url_update_redirect, HTTPStatus.FOUND
        )
        assert self.item_data.items() <= model_to_dict(item).items()

    def test_update_by_not_owner(self) -> None:
        """Test the item update, by not owner."""
        self.client.force_login(self.not_owner)
        response = self.client.post(self.url_update, self.item_data)
        item = self.manager.get(pk=self.item_pk)

        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )
        assert self.item_data.items() != model_to_dict(item).items()

    def test_update_by_anonymous(self) -> None:
        """Test the item update, by anonymous."""
        response = self.client.post(self.url_update, self.item_data)
        item = self.manager.get(pk=self.item_pk)

        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )
        assert self.item_data.items() != model_to_dict(item).items()


class DeleteTestMixin(TestMixinAnnotations):
    """Delete tests mixin."""

    def test_delete_get_method(self) -> None:
        """Test the item delete, get method."""
        self.client.force_login(self.owner)
        response = self.client.get(self.url_delete)
        assert response.status_code == HTTPStatus.OK

    def test_delete(self) -> None:
        """Test the item delete."""
        self.client.force_login(self.owner)
        response = self.client.post(self.url_delete)

        assert not self.manager.filter(pk=self.item_pk).exists()
        self.assertRedirects(
            response, self.url_delete_redirect, HTTPStatus.FOUND
        )

    def test_delete_not_owner(self) -> None:
        """Test the item delete, by not owner."""
        self.client.force_login(self.not_owner)
        response = self.client.post(self.url_delete)

        assert self.manager.filter(pk=self.item_pk).exists()
        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )
