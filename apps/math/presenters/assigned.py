"""Defines assigned calculation exercise presenter."""

import logging

from wse_exercises.core.math import CalcTask

from apps.core.storage.services.iabc import TaskStorageProto
from apps.study.servises.iabc import StrTaskCheckerProto
from apps.users.services.award import AwardService

from ..services.protocol import ExerciseServiceProto
from ..services.types import AssignedCalcAnswerType
from .base import BaseCalcTaskPresenter

logger = logging.getLogger(__name__)


class AssignedCalculationPresenter(
    BaseCalcTaskPresenter[AssignedCalcAnswerType],
):
    """Assigned calculation exercise presenter."""

    # TODO: Update `AwardService` to interface.
    def __init__(
        self,
        exercise_service: ExerciseServiceProto[CalcTask],
        task_storage: TaskStorageProto[CalcTask],
        task_checker: StrTaskCheckerProto,
        award_service: AwardService,
    ) -> None:
        """Construct the presenter."""
        super().__init__(
            exercise_service,
            task_storage,
            task_checker,
        )
        self._award_service = award_service
