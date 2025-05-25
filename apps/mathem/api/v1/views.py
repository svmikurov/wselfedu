"""Defines Math app REST API views."""

from dependency_injector import providers
from dependency_injector.wiring import Provide, inject
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from di.di_container import MainContainer
from services.exceptions import ExerciseServiceException
from services.exercise import ExerciseService


class ExerciseViewSet(ViewSet):
    """Exercise ViewSet with proper separation of concerns.

    Endpoints:
    POST /calculation/{exercise_type}/ - Generate exercise task
    """

    permission_classes = [permissions.AllowAny]

    @action(
        detail=False,
        methods=['post'],
        url_path=r'(?P<exercise_type>[a-zA-Z]+)',
    )
    @inject
    def create_task(
        self,
        request: Request,
        exercise_type: str,
        exercises_container: providers.DependenciesContainer = Provide[
            MainContainer.math.exercises
        ],
    ) -> Response:
        """Generate exercise task."""
        try:
            task_json = ExerciseService.create_task(
                exercises_container, exercise_type
            )
            return Response({'task': task_json}, status=200)

        except ExerciseServiceException as e:
            return self._handle_service_error(e)

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
