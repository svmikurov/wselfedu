"""Foreign word testing exercise."""

from django.db.models import Model, Q

from foreign.exercise.base import ExerciseItems
from foreign.models.word import AssignedWord, Word
from users.models import UserApp


class ItemTesting(ExerciseItems):
    """Item testing exercise."""

    _model: Model = AssignedWord

    def __init__(self, user: UserApp) -> None:
        """Construct the exercise."""
        self._user: UserApp = user
        self._item_count: int = 7
        self.task_item: Word | None = None
        self.task_item_id: int | None = None
        self.task_item_ids: list[int] | None = None

    def create_task(self) -> None:
        """Create task."""
        params = (Q(student=self._user),)
        item_ids = self._get_item_ids(self._model, params, id_field='word__pk')
        # fmt: off
        self.task_item_ids = self._get_random_item_ids(self._item_count, item_ids)  # noqa: E501
        self.task_item_id = self._get_random_item_id(self.task_item_ids)
        self.task_item = self._get_item(model=Word, pk=self.task_item_id)
        # fmt: on

    @property
    def task_data(self) -> dict:
        """Task data (`dict`, reqe-only)."""
        self.create_task()
        fields = 'id', 'foreign_word'
        items = self._get_items(Word, self.task_item_ids, fields)
        results = {
            'question': self.task_item.native_word,
            'answer': self.task_item_id,
            'choices': items,
        }
        return results
