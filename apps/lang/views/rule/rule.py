"""Language rule views."""

from dependency_injector.providers import Container
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views import generic

from apps.lang import models
from apps.lang.adapters import dto
from apps.lang.adapters.rule import WebRuleAdapter
from apps.lang.di import LanguageContainer
from di import MainContainer

from . import base
from ._data import CONTEXT

CONTAINER: Container[LanguageContainer] = MainContainer.lang


class RuleIndexView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/index.html'
    extra_context = CONTEXT['user_rule_index']


class RuleCreateView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/create/index.html'


class RuleDetailView(base.BaseRuleDetailView[dto.RuleSchema]):
    """Language rule detail view."""

    template_name = 'lang/rule/detail/index.html'
    extra_context = CONTEXT['rule_detail']

    def _get_rule_object(self) -> models.Rule:
        """Get rule object from repository."""
        return self.repository.get_for_user(self.user, self.rule_pk)

    def _convert_to_dto(self, rule_object: models.Rule) -> dto.RuleSchema:
        """Convert rule object to DTO."""
        return WebRuleAdapter.to_response(rule_object)


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
