"""Language discipline base views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from di import MainContainer

from ..repos.abc import TranslationRepoABC

if TYPE_CHECKING:
    from django.http.request import HttpRequest as HttpRequest
    from django.http.response import HttpResponseBase


class TranslationView(LoginRequiredMixin, View):
    """Base English translation view with repository injection."""

    repository: TranslationRepoABC | None = None

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
        self.repository = repository
        return super().dispatch(request, *args, **kwargs)
