"""View for managing student assignments."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from apps.core.views.auth import UserRequestMixin
from apps.lang import forms, models
from apps.lang.forms.queries import get_exercise_translations

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from django.http.request import HttpRequest
    from django.http.response import HttpResponseBase

# HACK: Refactor this code


class AssignedTranslationView(
    UserRequestMixin,
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """Assigned translations to exercise."""

    template_name = 'lang/exercise/mentor/translation/index.html'
    partial_template_name = 'lang/exercise/mentor/translation/_table.html'
    context_object_name = 'translations'
    paginate_by = 3

    @method_decorator(csrf_protect)
    def dispatch(
        self, request: HttpRequest, *args: object, **kwargs: object
    ) -> HttpResponseBase:
        """Add CSRF protection for POST request."""
        return super().dispatch(request, *args, **kwargs)

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
            return get_exercise_translations(self.user, int(exercise_id))
        return get_exercise_translations(self.user)

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
