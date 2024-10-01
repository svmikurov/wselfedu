"""Glossary exercise."""

from random import choice

from django.db.models import Model, Q

from glossary.models import Glossary
from task.orm_queries.glossary_lookup_params import GlossaryLookupParams


class GlossaryExercise:
    """Glossary exercise."""

    def __init__(self, lookup_conditions: dict) -> None:
        """Construct the exercise."""
        self.lookup_conditions = lookup_conditions
        self.model: Model = Glossary

    @property
    def _lookup_params(self) -> tuple[Q, ...]:
        """Encapsulated filters to lookup in query."""
        lookup_params = GlossaryLookupParams(self.lookup_conditions)
        return lookup_params.params

    def _get_item_ids(self) -> list[int]:
        """Get item ids by user lookup conditions."""
        item_ids = Glossary.objects.filter(
            *self._lookup_params
        ).values_list('id', flat=True)  # fmt: skip
        return item_ids

    @staticmethod
    def _get_random_item_id(item_ids: list) -> int:
        """Get random item for task."""
        return choice(item_ids)

    @staticmethod
    def _get_item(model: Model, pk: int) -> Model:
        """Get item model instance."""
        return model.objects.get(pk=pk)

    def create_exercise_task(self) -> Model:
        """Create task."""
        item_ids = self._get_item_ids()
        item_id = self._get_random_item_id(item_ids)
        item = self._get_item(model=self.model, pk=item_id)
        return item

    @property
    def task_data(self) -> dict:
        """Task data (`dict`, reqe-only)."""
        item = self.create_exercise_task()
        results = {
            'id': item.pk,
            'question_text': item.term,
            'answer_text': item.definition,
        }
        return results
