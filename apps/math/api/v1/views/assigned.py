"""Viewset to completion assigned Math exercises."""

from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.math.presenters.assigned import AssignedCalculationPresenter
from apps.study.selectors.iabc import IAssignedSelector
from apps.users.models import Person
from di import MainContainer as Container

from ..serializers import calculation as ser


class ExerciseViewSet(viewsets.ViewSet):
    """ViewSet for managing assigned math exercises.

    Provides endpoints for retrieving exercise tasks assigned to
    students.
    """

    @extend_schema(
        summary='Get assigned math exercise task',
        description='Returns a specific task from an assigned math exercise',
        parameters=[
            OpenApiParameter(
                name='exercise_slug',
                description='Unique exercise identifier (slug)',
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name='assignation_id',
                description='Exercise assignment ID for the student',
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            ),
        ],
        responses={
            HTTPStatus.OK: ser.ResultAnswerSerializer,
            HTTPStatus.NOT_FOUND: OpenApiResponse(
                description='Exercise or assignment not found',
                response=OpenApiTypes.OBJECT,
                examples=[
                    OpenApiExample(
                        'Error example',
                        value={'error': 'Exercise not found'},
                        status_codes=[HTTPStatus.NOT_FOUND],
                    )
                ],
            ),
        },
        tags=['Math'],
    )
    @action(
        methods=['get'],
        detail=False,
        url_path=r'exercise/(?P<exercise_slug>[-\w]+)',
        url_name='question',
    )
    @inject
    def exercise(
        self,
        request: Request,
        assignation_id: int,
        exercise_slug: str,
        exercise_selector: IAssignedSelector = Provide[
            Container.study.assigned_exercises_selector
        ],
        exercise_presenter: AssignedCalculationPresenter = Provide[
            Container.math.assigned_calc_presenter
        ],
    ) -> Response:
        """Render question of assigned exercise."""
        try:
            data = exercise_selector.select(
                assignation_id,
                exercise_slug,
                self.student,
            )

        except Exception as err:
            return Response(
                {
                    'status': 'error',
                    'message': str(err),
                },
                status=HTTPStatus.NOT_FOUND,
            )

        else:
            task = exercise_presenter.get_task(data)
            return Response(ser.QuestionSerializer(task).data)

    @extend_schema(
        request=ser.AssignedAnswerSerializer,
        responses={
            HTTPStatus.OK: ser.ResultAnswerSerializer,
        },
        tags=['Math'],
    )
    @action(
        methods=['post'],
        detail=False,
        url_name='check',
    )
    def check(
        self,
        request: Request,
        assignation_id: int,
        exercise_presenter: AssignedCalculationPresenter = Provide[
            Container.math.assigned_calc_presenter
        ],
    ) -> Response:
        """Render answer checking result."""
        # TODO: Add assignation validation with `get_object_or_404`
        # TODO: Add assignation available validation

        data = ser.AssignedAnswerSerializer(
            data=request.data,
            context={
                'assignation_id': assignation_id,
            },
        )
        data.is_valid()

        try:
            result = exercise_presenter.get_result(data.validated_data)

        except Exception as err:
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

    @property
    def student(self) -> Person:
        """Get current user."""
        student = self.request.user
        assert isinstance(student, Person)
        return student
