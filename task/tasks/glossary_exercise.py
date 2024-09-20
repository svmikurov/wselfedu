"""Glossary exercise.

Specific for rest api requests.
"""

from random import choice

from django.db.models import Model

from glossary.models import Glossary


class GlossaryExercise:
    """Glossary exercise."""

    def __init__(self, exercise_params: dict) -> None:
        """Construct the exercise."""
        self.exercise_params = exercise_params
        self.model: Model = Glossary

    @staticmethod
    def _get_item_ids() -> list[int]:
        """Get term ids by user conditions of the exercise.

        Returns
        -------
        term_ids : `list[int]`
            List of id term ids that satisfy the conditions of the
            exercise.

        Raises
        ------
        ValueError
            Raised if no terms that satisfy the conditions of the
            exercise.

        """
        item_ids = Glossary.objects.all().values_list('id', flat=True)
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
