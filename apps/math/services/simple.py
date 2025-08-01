"""Defines simple calculation exercise service."""

import logging
import uuid

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from typing_extensions import override
from wse_exercises.base.rest import CheckRequest, TaskRequest
from wse_exercises.core import MathEnum
from wse_exercises.core.math import (
    SimpleCalcAnswer,
    SimpleCalcConditions,
    SimpleCalcConfig,
    SimpleCalcQuestion,
    SimpleCalcTask,
)
from wse_exercises.core.math.rest import SimpleCalcResult

from apps.users.models import CustomUser
from apps.users.services.balance import BalanceService
from services.exercises.base import BaseExerciseService
from services.storage.interfaces import ICacheClient

from .db import SimpleCalcDBService
from .factories import IExerciseFactory
from .inspector import ITaskInspector

logger = logging.getLogger(__name__)


class SimpleCalcService(
    BaseExerciseService[
        MathEnum,
        SimpleCalcConfig,
        SimpleCalcConditions,
        SimpleCalcQuestion,
        SimpleCalcAnswer,
    ],
):
    """Mathematical simple calculation exercise with two operands."""

    def __init__(
        self,
        exercise_factory: IExerciseFactory,
        db: SimpleCalcDBService,
        cache: ICacheClient[SimpleCalcTask],
        inspector: ITaskInspector[int, int],
        balance_service: BalanceService,
    ) -> None:
        """Construct the exercise."""
        self._exercise_factory = exercise_factory
        self._db = db
        self._cache = cache
        self._inspector = inspector
        self._balance_service = balance_service

    @override
    def create(
        self,
        user: CustomUser | AnonymousUser,
        request_dto: TaskRequest[MathEnum, SimpleCalcConfig],
    ) -> tuple[uuid.UUID, SimpleCalcTask]:
        """Create and store the task."""
        exercise = self._exercise_factory.get(request_dto.name)
        task_dto = exercise.create_task(request_dto.config)

        # The task UID is used to retrieve the task for checking.
        # The reward task is recorded immediately in the database,
        # which allows tracking uncompleted tasks.
        if request_dto.is_rewardable:
            if not user.is_authenticated:
                raise PermissionDenied

            task_uid = self._db.save_rewardable(user, task_dto)

        else:
            task_uid = self._cache.set(task_dto)

        return task_uid, task_dto

    @override
    def check(
        self,
        user: CustomUser | AnonymousUser,
        request_dto: CheckRequest[SimpleCalcAnswer],
    ) -> SimpleCalcResult:
        """Check the user answer."""
        cache_uid = request_dto.uid
        task_dto = self._cache.pop(cache_uid)
        correct_answer = task_dto.answer.number
        user_answer = request_dto.answer.number

        is_correct = self._inspector.check(correct_answer, user_answer)
        response_dto = SimpleCalcResult(is_correct=is_correct)

        if not is_correct:
            response_dto = response_dto.with_correct_answer(task_dto)

        if request_dto.is_rewardable:
            pass

        if user.is_authenticated:
            db_uid = self._db.save(user, task_dto, user_answer, response_dto)

            if is_correct:
                self._balance_service.reward_for_simple_calc_task(
                    task_uid=db_uid,
                    user=user,
                    reward=10,
                )

        return response_dto
