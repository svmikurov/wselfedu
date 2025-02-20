"""Term exercise."""

from django.urls import reverse_lazy

from contrib.exercise import ExerciseData
from glossary.models import Term
from glossary.queries.lookup_params import TermLookupParams
from users.models import UserApp


class GlossaryExerciseGUI(ExerciseData):
    """Term exercise to do in mobile app."""

    model = Term
    lookup_params = TermLookupParams

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the exercise."""
        super().__init__(*args, **kwargs)

    def create_task(self) -> None:
        """Create task."""
        super().create_task()
        self.question_text = self.item.term
        self.answer_text = self.item.definition

    # TODO: Refactor, move to base class.
    def _query_item_progress(self) -> int:
        """Query the term progress study assessment."""
        default_progress_value = 0
        queryset = Term.objects.filter(
            user=UserApp.objects.get(pk=self.lookup_conditions['user_id']),
            term=self.item,
        )
        try:
            progress = int(queryset.last().progress)
        except AttributeError:
            progress = default_progress_value
        return progress


class GlossaryExercise(GlossaryExerciseGUI):
    """Term exercise to do in browser."""

    def __init__(self, lookup_conditions: dict) -> None:
        """Construct the exercise."""
        self._user_id = lookup_conditions.get('user_id')
        self.timeout = lookup_conditions.pop('timeout')
        super().__init__(lookup_conditions)

    @property
    def task_data(self) -> dict:
        """Task data to render in browser (`dict`, reqe-only)."""
        self.create_task()
        results = {
            'term_id': self.item.pk,
            'question_text': self.question_text,
            'answer_text': self.answer_text,
            'timeout': self.timeout,
            'term_count': len(self.item_ids),
            'progress': self.item.progress,
            'favorites_status': self.item.favorites,
            'favorites_url': reverse_lazy(
                'glossary:term_favorites_view_ajax',
                kwargs={'term_id': self.item.pk},
            ),
            'word_detail_link': reverse_lazy(
                'glossary:term_detail',
                kwargs={'pk': self.item.id},
            ),
            'knowledge_url': reverse_lazy(
                'glossary:progress',
                kwargs={'term_id': self.item.pk},
            ),
        }
        return results
