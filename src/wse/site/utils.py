"""Django site utils."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


def get_or_create_session_key(request: HttpRequest) -> str:
    """Return request session key."""
    if request.session.session_key is None:
        request.session.save()

    if not isinstance(request.session.session_key, str):
        raise ValueError('Session not initialized')

    return request.session.session_key
