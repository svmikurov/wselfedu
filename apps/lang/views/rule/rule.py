"""Language rule views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, QuerySet
from django.views import generic

from apps.lang import models

from ._data import CONTEXT


class RuleIndexView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/index.html'
    extra_context = CONTEXT['user_rule_index']


class RuleCreateView(generic.TemplateView):
    """Language rule create view."""

    template_name = 'lang/rule/create/index.html'


class RuleDetailView(generic.DetailView):  # type: ignore[type-arg]
    """Language rule detail view."""

    template_name = 'lang/rule/detail/index.html'
    extra_context = CONTEXT['rule_detail']
    context_object_name = 'rule'
    model = models.Rule

    def get_queryset(self) -> QuerySet[models.Rule]:
        """Get rule clauses with examples and exceptions."""
        examples_qs = models.RuleExample.objects.select_related(
            'question_translation__english',
            'answer_translation__english',
        )
        return (
            super()
            .get_queryset()
            .prefetch_related(
                Prefetch(
                    'clauses',
                    queryset=models.RuleClause.objects.prefetch_related(
                        Prefetch('examples', queryset=examples_qs)
                    ),
                )
            )
        )


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
