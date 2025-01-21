"""Base exercise."""

from random import choice

from django.db.models import Model, Q


class Exercise:
    """Base exercise."""

    lookup_params = None

    def __init__(self, lookup_conditions: dict) -> None:
        """Construct the exercise."""
        self.lookup_conditions = lookup_conditions
        self.item = None
        self.item_ids = None
        self.question_text = None
        self.answer_text = None
        self.is_first = lookup_conditions.pop('is_first')
        self.is_last = lookup_conditions.pop('is_last')
        self.count_first = lookup_conditions.pop('count_first')
        self.count_last = lookup_conditions.pop('count_last')

    @property
    def _lookup_params(self) -> tuple[Q, ...]:
        """Encapsulated filters to lookup in query."""
        return self.lookup_params(self.lookup_conditions).params

    # TODO: Optimize on ORM side.
    def _get_item_ids(self) -> list[int]:
        """Get item ids by user lookup conditions."""
        item_ids = self.model.objects.filter(*self._lookup_params).values_list(
            'id', flat=True
        )

        if self.is_first:
            first_items = list(
                item_ids.order_by('created_at')[: self.count_first]
            )
        else:
            first_items = []
        if self.is_last:
            last_items = list(
                item_ids.order_by('-created_at')[: self.count_last]
            )
        else:
            last_items = []

        first_items.extend(last_items)

        if first_items:
            return list(set(first_items))
        else:
            return item_ids

    @staticmethod
    def _get_random_item_id(item_ids: list) -> int:
        """Get random item for task."""
        return choice(item_ids)

    @staticmethod
    def _get_item(model: Model, pk: int) -> Model:
        """Get item model instance."""
        return model.objects.get(pk=pk)

    def create_task(self) -> None:
        """Create task."""
        self.item_ids = self._get_item_ids()
        item_id = self._get_random_item_id(self.item_ids)
        self.item = self._get_item(model=self.model, pk=item_id)

    @property
    def task_data(self) -> dict:
        """Task data (`dict`, reqe-only)."""
        self.create_task()
        results = {
            'id': self.item.pk,
            'question_text': self.question_text,
            'answer_text': self.answer_text,
        }
        return results


class ExerciseData(Exercise):
    """Task with additional data of exercise.

    Adds the additionally general exercise data to render the task.
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the exercise task."""
        super().__init__(*args, **kwargs)

    @property
    def task_data(self) -> dict[str, str]:
        """Exercise data (``dact``, reade-only)."""
        data = super().task_data
        data['item_count'] = len(self.item_ids)
        data['assessment'] = self._query_item_progress()
        return data

    def _query_item_progress(self) -> int:
        """Query the item progress study."""
        raise NotImplementedError(
            'Subclasses must provide a _get_item_progress() method.'
        )
