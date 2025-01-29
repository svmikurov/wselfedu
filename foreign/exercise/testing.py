"""Foreign word testing exercise."""

from typing import TypeVar

from django.db.models import Model, Q

from foreign.exercise.base import TestingItemsMixin
from foreign.models.word import AssignedWord, Word
from users.models import UserApp

ModelT = TypeVar('ModelT', bound=Model)

CHOICE_COUNT = 5


class ItemTesting(TestingItemsMixin):
    """Item testing exercise."""

    _assignations_model: ModelT = AssignedWord
    _item_model: ModelT = Word

    def __init__(self, user: UserApp) -> None:
        """Construct the exercise."""
        self._user: UserApp = user
        self._choice_count: int = CHOICE_COUNT
        self._task_item: ModelT | None = None
        self._task_item_id: int | None = None
        self._task_item_ids: list[int] | None = None
        self._fields: list[str] = ['id', 'foreign_word']
        self._choices: list = []

    def create_task(self) -> None:
        """Create task."""
        params = (Q(student=self._user),)
        item_ids = self._get_item_ids(
            self._assignations_model,
            params,
            id_field='word__pk',
        )
        self._task_item_ids = self._get_random_item_ids(
            self._choice_count,
            item_ids,
        )
        self._task_item_id = self._get_random_item_id(
            self._task_item_ids,
        )
        self._task_item = self._get_item(
            model=self._item_model,
            pk=self._task_item_id,
        )
        self._create_choices()

    @property
    def task_data(self) -> dict:
        """Task data (`dict`, read-only)."""
        self.create_task()
        results = {
            'question': self._task_item.native_word,
            'answer': self._task_item_id,
            'choices': self._choices,
        }
        return results
