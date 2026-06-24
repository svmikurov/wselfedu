"""Exercise page test."""

from __future__ import annotations

from http import HTTPStatus
from typing import TYPE_CHECKING

from django.urls import reverse

if TYPE_CHECKING:
    from django.test import Client


def test_exercise_page_returns_http_200(client: Client) -> None:
    url = reverse('testing')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
