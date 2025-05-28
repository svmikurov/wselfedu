"""Defines Math app REST API views."""

import logging

from dependency_injector.wiring import Provide, inject
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from wse_exercises.core.mathem.base.exercise import SimpleMathTaskRequest

from apps.mathem.di_container import MathContainer
from services.exceptions import (
    ExerciseServiceException,
)
from services.exercise import SimpleMathExerciseService

logger = logging.getLogger(__name__)


class CalculationViewSet(ViewSet):
    """Calculation exercise ViewSet."""

    permission_classes = [permissions.AllowAny]

    @action(
        detail=False,
        methods=['post'],
        url_path='simple',
    )
    @inject
    def render_task(
        self,
        request: Request,
        exercise_service: SimpleMathExerciseService = Provide[
            MathContainer.exercise_service
        ],  # type: ignore
    ) -> Response:
        """Generate exercise task."""
        task_request_dto = SimpleMathTaskRequest.model_validate(request.data)
        try:
            task_dto = exercise_service.create_task(task_request_dto)
        except ExerciseServiceException as e:
            return self._handle_service_error(e)
        return Response(task_dto.model_dump_json(), status=200)

    @classmethod
    def _handle_service_error(
        cls,
        error: ExerciseServiceException,
    ) -> Response:
        """Handle service layer error."""
        return Response(
            {'error': error.default_detail},
            status=error.status_code,
        )
