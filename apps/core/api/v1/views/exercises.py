"""Defines views for mentorship info."""
from functools import cached_property

from dependency_injector.wiring import Provide
from django.shortcuts import get_list_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api.v1.serializers.exercises import AssignedMentorSerializer
from apps.users.models import CustomUser
from apps.users.presenters import StudentExercisesPresenter
from di import MainContainer


class AssignedExercisesSetView(viewsets.ViewSet):
    """Assigned exercises viewset."""

    presenter: StudentExercisesPresenter = Provide[
        MainContainer.users_container.exercises_presenter,
    ]

    @extend_schema(
        summary='Get assigned exercises by mentor',
        description='Endpoint for assigned exercises by mentor',
        responses={200: AssignedMentorSerializer},
        tags=['Core'],
    )
    @action(detail=False, url_path='assigned-mentor')
    def assigned_mentor(self, request: Request) -> Response:
        """Render the exercises assigned by mentor."""
        serializer = AssignedMentorSerializer(
            self.presenter.get_assigned_exercise_all(self.user),
            many=True,
        )
        return Response(data=serializer.data)

    @cached_property
    def user(self) -> CustomUser:
        """Get mentorship instance."""
        user = self.request.user
        assert isinstance(user, CustomUser)
        return user
