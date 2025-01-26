"""Exercise elements."""

from random import choice
from typing import Any, Iterable, Type

from django.db.models import Model, Q

from config.constants import PROGRES_STEPS, PROGRESS_MAX, PROGRESS_MIN
from foreign.models import Word, WordProgress
from users.models import UserApp


class WordAssessment:
    """Assessment of item study."""

    def __init__(self, user: UserApp, data: dict) -> None:
        """Construct the assessment."""
        self.user = user
        self.word = Word.objects.get(pk=data['item_id'])
        self.action = data['action']

    def update(self) -> None:
        """Update item assessment."""
        assessment_delta = PROGRES_STEPS[self.action]
        progress, _ = WordProgress.objects.get_or_create(
            user=self.user, word=self.word
        )
        updated_assessment = progress.progress + assessment_delta

        if PROGRESS_MIN <= updated_assessment <= PROGRESS_MAX:
            progress.progress = updated_assessment
            progress.save(update_fields=['progress'])


# fmt: off
class ExerciseItems:
    """Get exercise items methods."""

    @staticmethod
    def _get_item_ids(
        model: Model,
        lookup_params: Iterable[Q],
        id_field: str,
    ) -> list[int]:
        item_ids = (
            model
            .objects
            .filter(*lookup_params)
            .values_list(id_field, flat=True)
        )
        return list(item_ids)

    @staticmethod
    def _get_random_item_ids(
        item_count: int,
        item_ids: list[int],
    ) -> list[int]:
        ids = [i for i in item_ids]
        task_ids = []
        # Random item ids have a certain amount in the task.
        for _ in range(item_count):
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

    @staticmethod
    def _get_items(
        model: Type[Model],
        item_ids: Iterable[int],
        fields: Iterable[str],
    ) -> list[tuple[Any, ...]]:
        return list(
            model
            .objects
            .filter(pk__in=item_ids)
            .values_list(*fields)
        )
# fmt: on
