"""Language discipline base views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject

from apps.users.models import Person
from di import MainContainer

from ..repositories.abc import TranslationRepoABC

if TYPE_CHECKING:
    from django.http.request import HttpRequest as HttpRequest
    from django.http.response import HttpResponseBase


class TranslationViewMixin:
    """Provides repository injection and user property."""

    _repository: TranslationRepoABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repository: TranslationRepoABC = Provide[
            MainContainer.lang.translation_repo
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject repository before processing request."""
        self._repository = repository
        return super().dispatch(request, *args, **kwargs)  # type: ignore[no-any-return, misc]

    @property
    def repository(self) -> TranslationRepoABC:
        """Get translation repository."""
        if not isinstance(self._repository, TranslationRepoABC):
            raise AttributeError('Repository not initialized')
        return self._repository

    @property
    def user(self) -> Person:
        """Get user."""
        return self.request.user  # type: ignore[attr-defined, no-any-return]
