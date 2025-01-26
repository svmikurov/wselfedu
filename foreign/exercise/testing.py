"""Foreign word testing exercise."""

# fmt: off
from random import choice
from typing import Type

from django.db.models import Model, Q

from foreign.models.word import AssignedWord, Word
from users.models import UserApp


class ItemTesting:
    """Item testing exercise."""

    _model: Model = AssignedWord

    def __init__(self, user: UserApp) -> None:
        """Construct the exercise."""
        self._user: UserApp = user
        self._item_count: int = 7
        self.task_item: Word | None = None
        self.task_item_id: int | None = None
        self.task_item_ids: list[int] | None = None

    @staticmethod
    def _get_item_ids(
        model: Model, lookup_params: tuple[Q, ...]
    ) -> list[int]:
        item_ids = (
            model.objects
            .filter(*lookup_params)
            .values_list('word__pk', flat=True)
        )
        return list(item_ids)

    def _get_random_item_ids(self, item_ids: list[int]) -> list[int]:
        ids = [i for i in item_ids]
        task_ids = []
        # Random item ids have a certain amount in the task.
        for _ in range(self._item_count):
            if not ids:
                break
            item_id = choice(ids)
            task_ids.append(item_id)
            ids.remove(item_id)
        return task_ids

    @staticmethod
    def _get_random_item_id(task_ids: list[int]) -> int:
        return choice(task_ids)

    @staticmethod
    def _get_item(model: Type[Model], pk: int) -> Model:
        return model.objects.get(pk=pk)

    def create_task(self) -> None:
        """Create task."""
        params = Q(student=self._user),
        item_ids = self._get_item_ids(self._model, params)
        self.task_item_ids = self._get_random_item_ids(item_ids)
        self.task_item_id = self._get_random_item_id(self.task_item_ids)
        self.task_item = self._get_item(model=Word, pk=self.task_item_id)  # noqa: E501

    @property
    def task_data(self) -> dict:
        """Task data (`dict`, reqe-only)."""
        self.create_task()
        items = (
            Word.objects
            .filter(pk__in=self.task_item_ids)
            .values_list('id', 'foreign_word')
        )
        results = {
            'question': self.task_item.native_word,
            'answer': self.task_item_id,
            'choices': list(items),
        }
        return results
