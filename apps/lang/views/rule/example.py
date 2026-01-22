"""Rule clause edit example/exception views."""

from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views import generic

from apps.core.views.auth import UserRequestMixin
from apps.core.views.crud import BaseAddView
from apps.core.views.htmx import HtmxOwnerDeleteView
from apps.lang import forms, models


class TaskExampleAddView(BaseAddView):
    """Add rule clause task example view."""

    form_class = forms.TaskExampleForm


class WordExampleAddView(BaseAddView):
    """Add rule clause word example view."""

    form_class = forms.WordExampleForm


class WordExampleListView(
    UserRequestMixin,
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Rule clause word example list view."""

    template_name = 'lang/rule/detail/_word_examples_edit.html'
    context_object_name = 'examples'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[models.RuleExample]:
        """Add filters and optimize query."""
        return (
            models.RuleExample.objects.filter(
                clause=self.kwargs['pk'],
                user=self.user,
            )
            .select_related(
                'translation__foreign',
                'translation__native',
            )
            .only(
                'translation__foreign__word',
                'translation__native__word',
            )
        )


class WordExampleDeleteView(HtmxOwnerDeleteView):
    """Rule clause word example delete view."""

    model = models.RuleExample


class TaskExampleListView(
    UserRequestMixin,
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Rule clause task example list view."""

    template_name = 'lang/rule/detail/_task_examples_edit.html'
    context_object_name = 'examples'
    paginate_by = 10

    def get_queryset(self) -> QuerySet[models.RuleTaskExample, Any]:
        """Add filters and optimize query."""
        return (
            models.RuleTaskExample.objects.filter(
                clause=self.kwargs['pk'],
                user=self.user,
            )
            .select_related(
                'question_translation__foreign',
                'answer_translation__foreign',
            )
            .only(
                'question_translation__foreign__word',
                'answer_translation__foreign__word',
            )
        )


class TaskExampleDeleteView(HtmxOwnerDeleteView):
    """Rule clause task example delete view."""

    model = models.RuleExample


class ExceptionAddView(BaseAddView):
    """Add rule clause word example view."""

    # TODO: Implement a view to add an exception to a rule clause
    # Add `form_class`
