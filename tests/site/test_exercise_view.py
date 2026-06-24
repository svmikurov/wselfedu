"""Exercise view tests."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client


def test_exercise_page_returns_http_200(client: Client) -> None:
    response = client.get(reverse('exercise'))
    assert response.status_code == HTTPStatus.OK
