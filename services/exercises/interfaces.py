"""Defines protocols for exercise services."""

import uuid
from typing import Any, Protocol, TypeVar

from django.contrib.auth.models import AnonymousUser
from wse_exercises.base.rest import (
    CheckRequest,
    CheckResponse,
    TaskRequest,
)
from wse_exercises.base.task import Task

from apps.users.models import CustomUser

TaskRequestT_contra = TypeVar(
    'TaskRequestT_contra',
    bound=TaskRequest[Any, Any],
    contravariant=True,
)
TaskT_co = TypeVar(
    'TaskT_co',
    bound=Task[Any, Any, Any, Any, Any],
    covariant=True,
)
CheckRequest_contra = TypeVar(
    'CheckRequest_contra',
    bound=CheckRequest[Any],
    contravariant=True,
)


class IExerciseService(
    Protocol[
        TaskRequestT_contra,
        TaskT_co,
        CheckRequest_contra,
    ],
):
    """Protocol for exercise service."""

    def create(
        self,
        user: CustomUser | AnonymousUser,
        task_request: TaskRequestT_contra,
    ) -> tuple[uuid.UUID, TaskT_co]:
        """Create the task.

        :param CustomUser | AnonymousUser user: The user performing
            the exercise.
        :param TaskRequest task_request: The DTO representing
            the task request data.
        :return: A tuple containing:
            - The unique identifier of the newly created task.
            - The DTO representing the created task.
        :rtype: uuid.UUID, Task
        """

    def check(
        self,
        user: CustomUser | AnonymousUser,
        check_request: CheckRequest_contra,
    ) -> CheckResponse:
        """Check the user answer.

        :param CustomUser | AnonymousUser user: The user.
        :param CheckRequest check_request: The DTO representing the
            result of answer checking.
        :return: The DTO representing the user answer check result.
        :rtype: CheckResponse
        """
