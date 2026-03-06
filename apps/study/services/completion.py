"""Assigned exercise completion service."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F

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
    def add_success(self, assignation_pk: int) -> None:
        """Add a successful attempt to solve the exercise."""
        content_type = ContentType.objects.get_for_model(self._manager.model)

        with transaction.atomic():
            ExerciseLog.objects.update_or_create(
                exercise_content_type=content_type,
                exercise_object_id=assignation_pk,
                defaults={
                    'success_count': F('success_count') + self.INCREMENT,
                },
                create_defaults={
                    'success_count': self.INCREMENT,
                },
            )

    @override
    @decorators.log_unimplemented_call
    def add_failure(self, assignation_pk: int) -> None:
        """Add an unsuccessful attempt to solve the exercise."""
