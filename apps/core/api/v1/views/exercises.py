"""Defines views for mentorship info."""

from functools import cached_property

from dependency_injector.wiring import Provide
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import CustomUser
from apps.users.presenters import StudentExercisesPresenter
from di import MainContainer

from ..serializers.exercises import AssignedMentorSerializer


class AssignedExercisesSetView(viewsets.ViewSet):
    """Assigned exercises viewset."""

    presenter: StudentExercisesPresenter = Provide[
        MainContainer.users_container.exercises_presenter,
    ]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Get assigned exercises by all mentors',
        description='Endpoint for assigned exercises by all mentors',
        responses={200: AssignedMentorSerializer(many=True)},
        tags=['Core'],
    )
    @action(detail=False, url_path='mentors/all-disciplines')
    def mentors_all_disciplines(self, request: Request) -> Response:
        """Render the exercises assigned by mentor."""
        queryset = self.presenter.get_assigned_all(self.user)
        serializer = AssignedMentorSerializer(queryset, many=True)
        return Response(data=serializer.data)

    @cached_property
    def user(self) -> CustomUser:
        """Get mentorship instance."""
        user = self.request.user
        assert isinstance(user, CustomUser)
        return user
