"""Defines abstract base class for exercises."""

import uuid
from abc import ABC, abstractmethod

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from typing_extensions import override
from wse_exercises import (
    AnswerT,
    ConditionsT,
    ConfigT,
    ExerciseT,
    QuestionT,
)
from wse_exercises.base.rest import (
    CheckRequest,
    CheckResponse,
    TaskRequest,
)
from wse_exercises.base.task import Task

from apps.users.models import CustomUser

from .interfaces import IExerciseService

User = get_user_model()


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
