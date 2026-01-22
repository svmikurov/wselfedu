"""Mentor exercise CRUD views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse_lazy
from django.views import generic

from apps.core.views import auth, crud, htmx
from apps.lang.forms import LangExerciseForm
from apps.lang.forms.queries import get_exercises
from apps.lang.models import LangExercise

if TYPE_CHECKING:
    from django.db.models import QuerySet

__all__ = [
    'MentorExerciseIndexView',
    'MentorExerciseListView',
    'MentorExerciseCreateView',
    'MentorExerciseUpdateView',
    'MentorExerciseDeleteView',
]


class MentorExerciseIndexView(
    auth.UserLoginRequiredMixin,
    generic.TemplateView,
):
    """Mentor exercises index view."""

    template_name = 'lang/exercise/mentor/index.html'


class MentorExerciseListView(
    auth.UserLoginRequiredMixin,
    crud.CsrfProtectMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Mentor exercises list view."""

    template_name = 'lang/exercise/mentor/management/index.html'
    context_object_name = 'exercises'

    def get_queryset(self) -> QuerySet[LangExercise]:
        """Get exercises queryset."""
        return get_exercises(self.user)


class MentorExerciseCreateView(
    auth.UserLoginRequiredMixin,
    crud.UserActionKwargsFormMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """Mentor exercise create view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:english_mentor_exercises_management')
    form_class = LangExerciseForm


class MentorExerciseUpdateView(
    auth.OwnershipRequiredMixin[LangExercise],
    crud.UserActionKwargsFormMixin,
    generic.UpdateView,  # type: ignore[type-arg]
):
    """Mentor exercise update view."""

    template_name = 'components/crispy_form.html'
    success_url = reverse_lazy('lang:english_mentor_exercises_management')
    model = LangExercise
    form_class = LangExerciseForm


class MentorExerciseDeleteView(
    htmx.HtmxOwnerDeleteView,
):
    """Mentor exercise delete view."""

    model = LangExercise
