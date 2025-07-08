"""Defines Mathematical application API views."""

import logging
from http import HTTPStatus
from typing import Any, Literal

from dependency_injector.wiring import Provide, inject
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from wse_exercises.base.rest import CheckResponse
from wse_exercises.core.math.rest import (
    SimpleCalcCheck,
    SimpleCalcRequest,
    SimpleCalcResponse,
)

from apps.users.services.interfaces import IBalanceService
from di.di_container import CoreContainer
from services.exercises.interfaces import IExerciseService

logger = logging.getLogger(__name__)


class SimpleCalcViewSet(viewsets.ViewSet):
    """Simple calculation task view."""

    permission_classes = [permissions.AllowAny]

    @inject
    @action(detail=False, methods=['post'], url_path='simple-calc')
    def create_task(
        self,
        request: Request,
        exercise_service: IExerciseService[Any, Any, Any] = Provide[
            CoreContainer.math_container.simple_calc_service
        ],
    ) -> Response:
        """Render the simple calculation task."""
        user = self.request.user

        try:
            request_dto = SimpleCalcRequest.from_dict(request.data)
        except ValueError as e:
            logger.exception('Validate error')
            return self._handle_error(e)

        # Create task

        try:
            uid, task_dto = exercise_service.create(user, request_dto)

        except ValueError as e:
            logger.exception('Task creation error')
            return self._handle_error(e)

        except PermissionDenied:
            logger.exception('Auth required for rewardable action')
            return self._handle_error(
                'Auth required', status_code=HTTPStatus.FORBIDDEN
            )

        else:
            response_dto = SimpleCalcResponse(uid=uid, task=task_dto)
            return Response(response_dto.to_dict(), status=self.success_status)

    @inject
    @action(detail=False, methods=['post'], url_path='simple-calc/validate')
    def check_answer(
        self,
        request: Request,
        exercise_service: IExerciseService[Any, Any, Any] = Provide[
            CoreContainer.math_container.simple_calc_service
        ],
    ) -> Response:
        """Render the result of answer check."""
        user = self.request.user

        try:
            request_dto = SimpleCalcCheck.from_dict(request.data)
        except ValueError as e:
            logger.exception('Validate error')
            return self._handle_error(e)

        try:
            response_dto: CheckResponse
            response_dto = exercise_service.check(user, request_dto)
        except (KeyError, ValueError) as e:
            logger.exception('Answer checking error')
            return self._handle_error(e)
        else:
            return Response(response_dto.to_dict(), status=self.success_status)

    # Utility methods

    @classmethod
    def _handle_error(
        cls,
        error: Exception | str,
        status_code: HTTPStatus = HTTPStatus.BAD_REQUEST,
    ) -> Response:
        """Render error response."""
        data = {'error': str(error)}
        return Response(data, status=status_code)

    # Property

    @property
    def success_status(self) -> Literal[200, 201]:
        """Get success status on answer check request.

        :return: Success HTTP status code:
            - 200 for anonymous user
            - 201 for authenticated user
        :rtype: Literal
        """
        return (
            status.HTTP_201_CREATED
            if self.request.user.is_authenticated
            else status.HTTP_200_OK
        )

    def finalize_response(
        self,
        request: Request,
        response: Response,
        *args: object,
        **kwargs: object,
    ) -> Response:
        """Add meta data to response."""
        if response.data is not None:
            response.data['meta'] = self._get_meta_data()
        return super().finalize_response(request, response, *args, **kwargs)

    def _get_meta_data(
        self,
        balance_service: IBalanceService = Provide[
            CoreContainer.math_container.balance_service
        ],
    ) -> dict[str, Any]:
        """Get meta data for response."""
        balance = balance_service.get_balance(self.request.user)
        print(f'{balance = }')
        return {'balance': balance}
