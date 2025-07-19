"""Defines protocol and abc for exercise service."""

import uuid
from abc import ABC, abstractmethod
from typing import Protocol

from django.contrib.auth.models import AnonymousUser
from typing_extensions import override
from wse_exercises import (
    AnswerT,
    ConditionsT,
    ConfigT,
    ExerciseT,
    QuestionT,
    TaskT_co,
)
from wse_exercises.base.rest import (
    CheckRequest,
    CheckRequest_contra,
    CheckResponse,
    TaskRequest,
    TaskRequestT_contra,
)
from wse_exercises.base.task import Task

from apps.users.models import CustomUser


class IExerciseService(
    Protocol[
        TaskRequestT_contra,
        TaskT_co,
        CheckRequest_contra,
    ],
):
    """Protocol for exercise service interface."""

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


class BaseExerciseService(
    IExerciseService[
        TaskRequest[ExerciseT, ConfigT],
        Task[ConfigT, ConditionsT, QuestionT, AnswerT, ExerciseT],
        CheckRequest[AnswerT],
    ],
    ABC,
):
    """Abstract base class for exercises."""

    @override
    @abstractmethod
    def create(
        self,
        user: CustomUser | AnonymousUser,
        task_request: TaskRequest[ExerciseT, ConfigT],
    ) -> tuple[
        uuid.UUID,
        Task[ConfigT, ConditionsT, QuestionT, AnswerT, ExerciseT],
    ]:
        """Create the task."""

    @override
    @abstractmethod
    def check(
        self,
        user: CustomUser | AnonymousUser,
        check_request: CheckRequest[AnswerT],
    ) -> CheckResponse:
        """Check the user answer."""
