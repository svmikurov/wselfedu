"""Language rule views."""

from functools import cached_property
from typing import Any

from dependency_injector.providers import Container
from dependency_injector.wiring import Provide, inject
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.views import generic

from apps.lang.adapters.rule import WebRuleAdapter, RuleSchema
from apps.core.views.auth import UserRequestMixin
from apps.lang import models
from apps.lang.di import LanguageContainer
from apps.lang.repositories import RuleRepositoryABC
from di import MainContainer

from ._data import CONTEXT

CONTAINER: Container[LanguageContainer] = MainContainer.lang


class RuleIndexView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/index.html'
    extra_context = CONTEXT['user_rule_index']


class RuleCreateView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/create/index.html'


class RuleDetailView(UserRequestMixin, generic.TemplateView):  # type: ignore[type-arg]
    """Language rule detail view."""

    template_name = 'lang/rule/detail/index.html'
    extra_context = CONTEXT['rule_detail']

    _repo: RuleRepositoryABC | None = None

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        repo: RuleRepositoryABC = Provide[CONTAINER.rule_repository],
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject rule repository."""
        self._repo = repo
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add data to context."""
        context = super().get_context_data(**kwargs)
        context['rule'] = self.rule
        return context

    @cached_property
    def rule(self) -> RuleSchema:
        """Get rule repository."""
        if self._repo is None:
            raise AttributeError('Repository not initialized')
        rule_q = self._repo.get_for_user(self.user, self.kwargs['pk'])
        rule_dto = WebRuleAdapter.to_response(rule_q)
        return rule_dto


class RuleUpdateView(generic.TemplateView):
    """Language rule update view."""

    template_name = 'lang/rule/update/index.html'


class RuleListView(LoginRequiredMixin, generic.ListView):  # type: ignore[type-arg]
    """Language rule list view."""

    template_name = 'lang/rule/list/index.html'
    extra_context = CONTEXT['rule_list']
    context_object_name = 'rules'

    def get_queryset(self) -> QuerySet[models.Rule]:
        """Get rule queryset."""
        return models.Rule.objects.filter(  # type: ignore[misc]
            user=self.request.user,
        )


class RuleDeleteView(generic.TemplateView):
    """Language rule delete view."""
