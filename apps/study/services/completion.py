"""Assigned exercise completion service."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.contrib.contenttypes.models import ContentType

from apps.study.models import ExerciseLog
from apps.study.services.abstract import (
    AbstractCompletionService,
    ExerciseAssignationModel,
)
from utils import decorators

if TYPE_CHECKING:
    from django.db.models import Manager

__all__ = ('ExerciseCompletionService',)


class ExerciseCompletionService(
    AbstractCompletionService[ExerciseAssignationModel]
):
    """Assigned exercise completion service.

    Updates assigned exercise performing log.
    """

    INCREMENT = 1
    """Exercise success solution count increment.
    """

    def __init__(self, manager: Manager[ExerciseAssignationModel]) -> None:
        """Construct the service."""
        self._manager = manager

    # TODO: Implement add_failure() method
    # Add private common method for count update
    # with model filed name to update

    @override
    def add_success(self, assignation_pk: int) -> int:
        """Add a successful attempt to solve the exercise."""
        content_type = ContentType.objects.get_for_model(self._manager.model)
        return self._make_raw_update(
            content_type, assignation_pk, self.INCREMENT
        )

    @override
    @decorators.log_unimplemented_call
    def add_failure(self, assignation_pk: int) -> None:
        """Add an unsuccessful attempt to solve the exercise."""

    def _make_raw_update(
        self,
        content_type: ContentType,
        object_id: int,
        increment: int,
    ) -> int:
        from django.db import connection

        with connection.cursor() as cursor:
            # Execute UPDATE with RETURNING
            cursor.execute(
                """
                UPDATE {table}
                SET success_count = success_count + %s
                WHERE exercise_content_type_id = %s
                    AND exercise_object_id = %s
                RETURNING success_count
                """.format(table=ExerciseLog._meta.db_table),
                [increment, content_type.id, object_id],
            )
            result = cursor.fetchone()

            if result:
                return result[0]  # type: ignore[no-any-return]
            else:
                log = ExerciseLog.objects.create(
                    exercise_content_type=content_type,
                    exercise_object_id=object_id,
                    success_count=increment,
                )
                return log.success_count
