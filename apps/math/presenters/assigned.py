"""Defines assigned calculation exercise presenter."""

import logging

from typing_extensions import override
from wse_exercises.core.math import CalcTask

from apps.core.storage.services.iabc import TaskStorageProto
from apps.core.types import RelatedDataType
from apps.study.servises.iabc import StrTaskCheckerProto
from apps.users.services.award import AwardService

from ..services.protocol import ExerciseServiceProto
from ..services.types import AssignedCalcAnswerType
from .base import BaseCalcTaskPresenter
from .types import ResultResponseType

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

    @override
    def get_result(
        self,
        data: AssignedCalcAnswerType,
    ) -> ResultResponseType:
        """Get user answer checking result."""
        payload = super().get_result(data)

        if payload['data']['is_correct'] and self._assignation_id is not None:
            try:
                balance = self._award_service.reward(self._assignation_id)
            except Exception:
                logger.exception('Update balance error')
            else:
                related_data: RelatedDataType = {
                    'balance': balance,
                }
                payload['related_data'] = related_data

        return payload
