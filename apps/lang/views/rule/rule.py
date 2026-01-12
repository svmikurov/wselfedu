"""Language rule views."""

from typing import Any

from dependency_injector.providers import Container
from django.db.models import Exists, OuterRef, QuerySet
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from apps.core.views.auth import OwnershipRequiredMixin, UserRequestMixin
from apps.lang import forms, models
from apps.lang.adapters import dto
from apps.lang.di import LanguageContainer
from apps.users.models import Mentorship
from di import MainContainer

from . import base
from ._data import CONTEXT

CONTAINER: Container[LanguageContainer] = MainContainer.lang


class RuleIndexView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/index.html'


class RuleCreateView(generic.CreateView):  # type: ignore[type-arg]
    """Language rule create view."""

    template_name = 'lang/rule/list/_rule_form.html'
    form_class = forms.RuleForm


class RuleDetailView(base.BaseRuleDetailView[dto.RuleSchema]):
    """Language rule detail view."""

    template_name = 'lang/rule/detail/index.html'
    extra_context = CONTEXT['rule_detail']

    def _get_rule_object(self) -> models.Rule:
        """Get rule object from repository."""
        return self.repository.get_for_user(self.user, self.rule_pk)

    def _convert_to_dto(self, rule_object: models.Rule) -> dto.RuleSchema:
        """Convert rule object to DTO."""
        return self.adapter.to_response(rule_object)


class RuleUpdateView(OwnershipRequiredMixin[models.Rule], generic.UpdateView):  # type: ignore[type-arg]
    """Language rule update view."""

    template_name = 'lang/rule/detail/_form.html'
    form_class = forms.RuleForm
    model = models.Rule


class ClauseCreateView(UserRequestMixin, generic.CreateView):  # type: ignore[type-arg]
    """Create rule clause view."""

    template_name = 'lang/rule/detail/_form.html'
    form_class = forms.ClauseForm

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add data to form."""
        kwargs = super().get_form_kwargs()

        rule = get_object_or_404(
            models.Rule,
            pk=self.kwargs['pk'],
            user=self.user,
        )
        form_action = reverse(
            'lang:english_clause_create',
            kwargs={'pk': rule.pk},
        )

        kwargs['user'] = self.user
        kwargs['rule'] = rule
        kwargs['form_action'] = form_action
        return kwargs

    def get_success_url(self) -> str:
        """Get success url."""
        return self.object.rule.get_absolute_url()  # type: ignore[no-any-return, union-attr]


class ClauseUpdateView(
    OwnershipRequiredMixin[models.RuleClause],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """Update rule clause view."""

    template_name = 'lang/rule/detail/_form.html'
    form_class = forms.ClauseForm
    model = models.RuleClause

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add data to form."""
        kwargs = super().get_form_kwargs()
        form_action = reverse(
            'lang:english_clause_update',
            kwargs={'pk': self.object.pk},
        )
        kwargs['rule'] = self.object.rule
        kwargs['user'] = self.user
        kwargs['form_action'] = form_action
        return kwargs

    def get_success_url(self) -> str:
        """Return clause rule detail url path."""
        return self.object.rule.get_absolute_url()  # type: ignore[no-any-return]


class RuleListView(UserRequestMixin, generic.ListView):  # type: ignore[type-arg]
    """Language rule list view."""

    template_name = 'lang/rule/list/index.html'
    extra_context = CONTEXT['rule_list']
    context_object_name = 'rules'

    def get_queryset(self) -> QuerySet[models.Rule]:
        """Get rule list queryset."""
        mentor_exists = Exists(
            Mentorship.objects.filter(mentor=OuterRef('user'))
        )
        student_exists = Exists(
            Mentorship.objects.filter(student=OuterRef('user'))
        )
        return (
            models.Rule.objects.filter(user=self.user)
            .select_related('user')
            .annotate(
                user_is_mentor=mentor_exists,
                user_is_student=student_exists,
            )
            .only('id', 'title', 'user_id')
        )


class RuleDeleteView(generic.TemplateView):
    """Language rule delete view."""
