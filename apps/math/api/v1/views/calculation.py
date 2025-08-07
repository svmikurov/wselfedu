"""Defines Math app calculation exercise viewset."""

from dependency_injector.wiring import Provide
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.math.presenters.calculation import CalcPresenter
from di import MainContainer

from ..serializers.calculation import (
    CalcAnswerSerializer,
    CalcDataSerializer,
    CalcResultSerializer,
    CalcTaskSerializer,
)


class CalculationViewSet(viewsets.ViewSet):
    """Math app calculation exercise viewset."""

    calc_exercise_presenter: CalcPresenter = Provide[
        MainContainer.math_container.calc_presenter
    ]

    @extend_schema(
        summary='Get calculation task',
        description='Endpoint for mathematical calculations exercise',
        request=CalcDataSerializer,
        responses={200: CalcTaskSerializer},
        tags=['Math'],
    )
    @action(detail=False, methods=['post'])
    def calculation(self, request: Request) -> Response:
        """Render the Math app calculation task."""
        data = CalcDataSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        task = self.calc_exercise_presenter.get_task(data.validated_data)
        return Response(CalcTaskSerializer(task).data)

    @extend_schema(
        summary='Check user answer on calculation task',
        description="Endpoint for checking user's answer to task",
        request=CalcAnswerSerializer,
        responses={200: CalcResultSerializer},
        tags=['Math'],
    )
    @action(detail=False, methods=['post'], url_path='calculation/validate')
    def calculation_validate(self, request: Request) -> Response:
        """Render the result of answer check."""
        data = CalcAnswerSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        result = self.calc_exercise_presenter.get_result(data.validated_data)
        return Response(CalcResultSerializer(result).data)
