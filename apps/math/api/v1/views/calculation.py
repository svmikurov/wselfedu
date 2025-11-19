"""Defines Math app calculation exercise viewset."""

import logging
from http import HTTPStatus

from dependency_injector.wiring import Provide
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api import renderers
from apps.math.presenters.calculation import CalculationPresenter
from di import MainContainer as Container

from ..serializers import calculation as ser

logger = logging.getLogger(__name__)


class CalculationViewSet(viewsets.ViewSet):
    """Math app calculation exercise ViewSet."""

    renderer_classes = [renderers.WrappedJSONRenderer]

    exercise_presenter: CalculationPresenter = Provide[
        Container.math.calc_presenter
    ]

    @extend_schema(
        summary='Get calculation task',
        description='Endpoint for mathematical calculations exercise',
        request=ser.ConditionSerializer,
        responses={
            HTTPStatus.OK: ser.QuestionSerializer,
        },
        tags=['Math'],
    )
    @action(
        detail=False,
        methods=['post'],
    )
    def calculation(self, request: Request) -> Response:
        """Render the Math app calculation task."""
        data = ser.ConditionSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        task = self.exercise_presenter.get_task(data.validated_data)
        return Response(ser.QuestionSerializer(task).data)

    @extend_schema(
        summary='Check user answer on calculation task',
        description="Endpoint for checking user's answer to task",
        request=ser.AnswerSerializer,
        responses={
            HTTPStatus.OK: ser.ResultAnswerSerializer,
        },
        tags=['Math'],
    )
    @action(
        detail=False,
        methods=['post'],
        url_path='calculation/validate',
    )
    def calculation_validate(self, request: Request) -> Response:
        """Render the result of answer check."""
        data = ser.AnswerSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        try:
            result = self.exercise_presenter.get_result(data.validated_data)

        # TODO: Fix response
        except Exception as err:
            logger.exception('Got result error')
            return Response(
                {
                    'status': 'error',
                    'message': str(err),
                },
                status=HTTPStatus.NOT_FOUND,
            )

        return Response(
            ser.ResultAnswerSerializer(result).data,
            status=HTTPStatus.OK,
        )
