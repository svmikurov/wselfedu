"""Defines Math app calculation exercise viewset."""

from typing import Annotated

from dependency_injector.wiring import Provide, inject
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

    @extend_schema(
        summary='Get calculation task',
        description='Endpoint for mathematical calculations exercise',
        request=CalcDataSerializer,
        responses={
            200: CalcTaskSerializer,
        },
        tags=['Math'],
    )
    @inject
    @action(detail=False, methods=['post'], url_path='simple-calc')
    def calculation(
        self,
        request: Request,
        presenter: Annotated[
            CalcPresenter,
            Provide[MainContainer.math_container.calc_presenter],
        ],
    ) -> Response:
        """Render the Math app calculation task."""
        data = CalcDataSerializer(request.data)
        task = presenter.get_task(data.data)
        serializer = CalcTaskSerializer(task)
        return Response(serializer.data)

    @extend_schema(
        summary='Check user answer on calculation task',
        tags=['Math'],
        responses=CalcAnswerSerializer,
        request=CalcResultSerializer,
    )
    @action(detail=False, methods=['post'], url_path='simple-calc/validate')
    def validate(
        self,
        request: Request,
        presenter: Annotated[
            CalcPresenter,
            Provide[MainContainer.math_container.calc_presenter],
        ],
    ) -> Response:
        """Render the result of answer check."""
        data = CalcAnswerSerializer(request.data)
        result = presenter.get_result(data.data)
        serializer = CalcResultSerializer(result)
        return Response(serializer.data)
