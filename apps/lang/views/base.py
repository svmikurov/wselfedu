"""Language discipline base views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from dependency_injector.wiring import Provide, inject
from django.views import generic

from apps.core import views as core_views
from di import MainContainer

from .. import repositories as repos

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase


class SettingsRepositoryBaseView(
    core_views.UserRequestMixin,
    generic.TemplateView,
):
    """Settings repository base view."""

    _repository: repos.WordStudyParamsRepositoryABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repository: repos.WordStudyParametersRepository = Provide[
            MainContainer.lang.parameters_repository,
        ],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject settings repository."""
        self._repository = repository
        return super().dispatch(request, *args, **kwargs)

    @property
    def repository(self) -> repos.WordStudyParametersRepository:
        """Get settings repository."""
        if not isinstance(
            self._repository, repos.WordStudyParametersRepository
        ):
            raise AttributeError('Repository not initialized')
        return self._repository
