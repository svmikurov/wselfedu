"""Assigned exercises viewset."""

from functools import cached_property
from http import HTTPStatus

from dependency_injector.wiring import Provide
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import CustomUser
from apps.users.presenters import StudentExercisesPresenter
from di import MainContainer

from ..serializers import (
    AssignedMentorSerializer,
    SelectExerciseSerializer,
)


class AssignedExercisesViewSet(viewsets.ViewSet):
    """Assigned exercises viewset."""

    permission_classes = [permissions.IsAuthenticated]

    presenter: StudentExercisesPresenter = Provide[
        MainContainer.users_container.exercises_presenter,
    ]

    @extend_schema(
        summary='Get assigned exercises by all mentors',
        description='Endpoint for assigned exercises by all mentors',
        responses={HTTPStatus.OK: AssignedMentorSerializer},
        tags=['Study'],
    )
    def list(self, request: Request) -> Response:
        """Render the exercises assigned by mentor."""
        queryset = self.presenter.get_assigned_all(self.user)
        serializer = AssignedMentorSerializer(queryset, many=True)
        return Response(data=serializer.data)

    @extend_schema(
        summary='Get meta data of selected exercise from assigned',
        description='Endpoint to get meta data of selected exercise',
        responses={HTTPStatus.OK: SelectExerciseSerializer},
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='Exercise assignment ID',
            ),
        ],
        tags=['Study'],
    )
    def retrieve(self, request: Request, pk: int) -> Response:
        """Handle the exercise choice of student."""
        queryset = self.presenter.get_exercise_meta(
            assignation_id=pk,
            student=self.user,
        )
        serializer = SelectExerciseSerializer(queryset)
        return Response(data=serializer.data)

    @cached_property
    def user(self) -> CustomUser:
        """Get mentorship instance."""
        user = self.request.user
        assert isinstance(user, CustomUser)
        return user
