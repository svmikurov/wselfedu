"""CRUD test mixins."""

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.db.models.manager import Manager
from django.forms import model_to_dict
from django.test import Client, TestCase

from contrib.tests.extension import flash_message_test
from users.models import UserApp

if TYPE_CHECKING:
    from django.test.client import (
        _MonkeyPatchedWSGIResponse as TestHttpResponse,
    )


class TestData(TestCase):
    """General test data.

    Inherit it to setUp the test data.
    """

    success_create_msg = ''
    success_update_msg = ''
    success_delete_msg = ''
    no_permission_msg = ''


class TestMixinAnnotations:
    """Test mixins annotations."""

    client: Client
    owner: UserApp
    owner_id: int
    not_owner: UserApp
    manager: Manager
    item_pk: int
    item_data: dict

    url_create: str
    url_list: str
    url_update: str
    url_detail: str
    url_delete: str
    url_create_redirect: str
    url_update_redirect: str
    url_detail_redirect: str
    url_delete_redirect: str
    url_not_owner_redirect: str


class TestMessageMixin:
    """Test message mixin."""

    success_create_msg: str
    success_update_msg: str
    success_delete_msg: str
    no_permission_msg: str

    @staticmethod
    def check_message(response: 'TestHttpResponse', msg: str) -> None:
        """Test the response message."""
        if msg:
            flash_message_test(response, msg)


class BaseTest(TestMixinAnnotations, TestMessageMixin):
    """Base test."""


class CreateTest(BaseTest):
    """Create tests."""

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

        self.check_message(response, self.success_create_msg)

    def test_create_by_anonymous(self) -> None:
        """Test the item create, by anonymous."""
        response = self.client.post(self.url_create, self.item_data)

        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )

        self.check_message(response, self.no_permission_msg)


class ListTest(BaseTest):
    """List tests."""

    def test_list(self) -> None:
        """Test the item list."""
        self.client.force_login(self.owner)
        response = self.client.get(self.url_list)

        assert response.status_code == HTTPStatus.OK

        # Assert by user id, that ``items`` contains only the user's
        # categories.
        items = response.context['object_list']
        user_ids = set(items.values_list('user', flat=True))
        self.assertTrue(*user_ids, self.owner_id)

    def test_list_anonymous(self) -> None:
        """Test the item list, for anonymous."""
        response = self.client.get(self.url_list)

        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )

        self.check_message(response, self.no_permission_msg)


class UpdateTest(BaseTest):
    """Update tests."""

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

        self.check_message(response, self.success_update_msg)

    def test_update_by_not_owner(self) -> None:
        """Test the item update, by not owner."""
        self.client.force_login(self.not_owner)
        response = self.client.post(self.url_update, self.item_data)
        item = self.manager.get(pk=self.item_pk)

        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )
        assert self.item_data.items() != model_to_dict(item).items()

        self.check_message(response, self.no_permission_msg)

    def test_update_by_anonymous(self) -> None:
        """Test the item update, by anonymous."""
        response = self.client.post(self.url_update, self.item_data)
        item = self.manager.get(pk=self.item_pk)

        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )
        assert self.item_data.items() != model_to_dict(item).items()

        self.check_message(response, self.no_permission_msg)


class DeleteTest(BaseTest):
    """Delete tests."""

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

        self.check_message(response, self.success_delete_msg)

    def test_delete_not_owner(self) -> None:
        """Test the item delete, by not owner."""
        self.client.force_login(self.not_owner)
        response = self.client.post(self.url_delete)

        assert self.manager.filter(pk=self.item_pk).exists()
        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )

        self.check_message(response, self.no_permission_msg)

    def test_delete_anonymous(self) -> None:
        """Test the item delete, by anonymous."""
        response = self.client.post(self.url_delete)

        assert self.manager.filter(pk=self.item_pk).exists()
        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )

        self.check_message(response, self.no_permission_msg)


class DetailTest(BaseTest):
    """Detail tests."""

    def test_detail(self) -> None:
        """Test the item detail."""
        self.client.force_login(self.owner)
        response = self.client.get(self.url_detail)
        assert response.status_code == HTTPStatus.OK

    def test_detail_for_not_owner(self) -> None:
        """Test the item detail, for not owner."""
        self.client.force_login(self.not_owner)
        response = self.client.get(self.url_detail)
        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )

    def test_detail_for_anonymous(self) -> None:
        """Test the item detail, for anonymous."""
        self.client.force_login(self.not_owner)
        response = self.client.get(self.url_detail)
        self.assertRedirects(
            response, self.url_not_owner_redirect, HTTPStatus.FOUND
        )