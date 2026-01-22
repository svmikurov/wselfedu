"""View for managing student assignments."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import transaction
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from apps.core import views as core_views
from apps.lang import forms, models
from apps.lang.forms import queries

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http.request import HttpRequest

    from apps.users.models import Person

# HACK: Refactor this code

# --------------------------
# Mentor exercise management
# --------------------------


class MentorExercisesIndexView(
    core_views.UserLoginRequiredMixin,
    generic.TemplateView,
):
    """Mentor exercises index view."""

    template_name = 'lang/exercise/mentor/index.html'


class MentorExerciseListView(
    core_views.UserLoginRequiredMixin,
    core_views.CsrfProtectMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Mentor exercises list view."""

    template_name = 'lang/exercise/mentor/management/index.html'
    context_object_name = 'exercises'

    def get_queryset(self) -> QuerySet[models.LangExercise]:
        """Get exercises queryset."""
        return queries.get_exercises(self.user)


class MentorExerciseCreateView(
    core_views.UserLoginRequiredMixin,
    core_views.UserActionKwargsFormMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """Mentor exercise create view."""

    template_name = 'components/crispy_form.html'
    form_class = forms.LangExerciseForm
    success_url = reverse_lazy('lang:english_mentor_exercises_management')


class MentorExerciseUpdateView(
    core_views.UserActionKwargsFormMixin,
    core_views.OwnershipRequiredMixin[models.LangExercise],
    generic.UpdateView,  # type: ignore[type-arg]
):
    """Mentor exercise update view."""

    template_name = 'components/crispy_form.html'
    model = models.LangExercise
    form_class = forms.LangExerciseForm
    success_url = reverse_lazy('lang:english_mentor_exercises_management')


class MentorExerciseDeleteView(core_views.HtmxOwnerDeleteView):
    """Mentor exercise delete view."""

    model = models.LangExercise


# --------------------------------------
# Mentor exercise assignation management
# --------------------------------------


class ExerciseAssignationCreateView(
    core_views.UserLoginRequiredMixin,
    core_views.UserActionKwargsFormMixin,
    generic.CreateView,  # type: ignore[type-arg]
):
    """Exercise assignation create view."""

    template_name = 'components/crispy_form.html'
    form_class = forms.ExerciseAssignationForm
    success_url = reverse_lazy('lang:english_mentor_exercises_management')


class ExerciseAssignationListView(
    core_views.UserLoginRequiredMixin,
    core_views.CsrfProtectMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Exercise assignation list view."""

    template_name = 'lang/exercise/mentor/assignation/index.html'
    context_object_name = 'assignations'

    def get_queryset(self) -> QuerySet[models.EnglishAssignedExercise]:
        """Get exercises queryset."""
        return queries.get_assignations(self.user)


class EnglishAssignedExerciseDeleteView(core_views.HtmxDeleteView):
    """Mentor exercise delete view."""

    model = models.EnglishAssignedExercise

    def _get_owner(self) -> Person:
        obj = self.get_object()
        return obj.mentorship.mentor  # type: ignore[no-any-return]


class AssignedTranslationView(
    core_views.UserLoginRequiredMixin,
    core_views.CsrfProtectMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Assigned translations to exercise.

    Adds translation to exercises.
    """

    template_name = 'lang/exercise/mentor/translation/index.html'
    partial_template_name = 'lang/exercise/mentor/translation/_table.html'
    context_object_name = 'translations'
    paginate_by = 15

    def get_template_names(self) -> list[str]:
        """Return partial template for HTMX queries."""
        if self.request.headers.get('HX-Request'):
            return [self.partial_template_name]
        return super().get_template_names()

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:  # type: ignore[override]
        """Add data to context."""
        context = super().get_context_data(**kwargs)  # type: ignore[arg-type]
        context['translation_ids'] = [t.id for t in context['object_list']]
        context['form'] = forms.AssignTranslationForm(user=self.user)
        return context

    def get_queryset(self) -> QuerySet[models.EnglishTranslation]:
        """Get translations queryset."""
        if exercise_id := self.request.GET.get('exercise_id', None):
            return queries.get_exercise_translations(
                self.user, int(exercise_id)
            )
        return queries.get_exercise_translations(self.user)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Update assignations."""
        data = request.POST

        exercise_id = int(data['exercise_id'])
        if ids_str := data.get('page_translation_ids'):
            translation_ids = [
                int(id_.strip()) for id_ in ids_str.split(',') if id_.strip()
            ]
        else:
            translation_ids = []

        prefix = 'active:'
        active_translation_ids = [
            int(name[len(prefix) :])
            for name in data
            if name.startswith(prefix)
        ]

        self.update_page_translations(
            exercise_id, translation_ids, active_translation_ids
        )

        return HttpResponse('Updated')

    @transaction.atomic
    def update_page_translations(
        self,
        exercise_id: int,
        translation_ids: list[int],
        active_translation_ids: list[int],
    ) -> None:
        """Обновляем только переводы на текущей странице."""
        all_set = set(translation_ids)
        active_set = set(active_translation_ids)

        to_remove = all_set - active_set
        models.EnglishExerciseTranslation.objects.filter(
            exercise_id=exercise_id, translation_id__in=to_remove
        ).delete()

        to_add = active_set
        existing = models.EnglishExerciseTranslation.objects.filter(
            exercise_id=exercise_id, translation_id__in=to_add
        ).values_list('translation_id', flat=True)

        new_ids = to_add - set(existing)
        if new_ids:
            models.EnglishExerciseTranslation.objects.bulk_create(
                [
                    models.EnglishExerciseTranslation(
                        exercise_id=exercise_id, translation_id=tid
                    )
                    for tid in new_ids
                ]
            )
