"""Language rule view for student."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from apps.core.views.auth import UserRequestMixin
from apps.lang.forms import RuleAssignmentForm
from apps.lang.models import Rule


class RuleAssignmentCreate(
    UserRequestMixin,
    LoginRequiredMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """Language rule assignment create view."""

    template_name = 'lang/rule/mentorship/index.html'
    form_class = RuleAssignmentForm

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add request and rule id to form kwargs."""
        kwargs = super().get_form_kwargs()

        rule = get_object_or_404(
            Rule,
            pk=self.kwargs['pk'],
            user=self.user,
        )

        kwargs['user'] = self.user
        kwargs['rule'] = rule
        return kwargs

    def get_success_url(self) -> str:
        """Get success url."""
        return str(reverse_lazy('lang:english_rule_list'))
