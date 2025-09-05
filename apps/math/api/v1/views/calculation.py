"""Defines Math app calculation exercise viewset."""

from http import HTTPStatus

from dependency_injector.wiring import Provide
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.math.presenters.calculation import CalculationPresenter
from di import MainContainer

from ..serializers.calculation import (
    AnswerSerializer,
    CheckSerializer,
    ConditionSerializer,
    TaskSerializer,
)


class CalculationViewSet(viewsets.ViewSet):
    """Math app calculation exercise viewset."""

    exercise_presenter: CalculationPresenter = Provide[
        MainContainer.math_container.calc_presenter
    ]

    @extend_schema(
        summary='Get calculation task',
        description='Endpoint for mathematical calculations exercise',
        request=ConditionSerializer,
        responses={
            HTTPStatus.OK: TaskSerializer,
        },
        tags=['Math'],
    )
    @action(
        detail=False,
        methods=['post'],
    )
    def calculation(self, request: Request) -> Response:
        """Render the Math app calculation task."""
        data = ConditionSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        task = self.exercise_presenter.get_task(data.validated_data)
        return Response(TaskSerializer(task).data)

    @extend_schema(
        summary='Check user answer on calculation task',
        description="Endpoint for checking user's answer to task",
        request=AnswerSerializer,
        responses={
            HTTPStatus.OK: CheckSerializer,
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
        data = AnswerSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        try:
            result = self.exercise_presenter.get_result(data.validated_data)

        # TODO: Fix response
        except Exception as err:
            return Response(
                {
                    'status': 'error',
                    'message': str(err),
                },
                status=HTTPStatus.NOT_FOUND,
            )

        return Response(
            CheckSerializer(result).data,
            status=HTTPStatus.OK,
        )
