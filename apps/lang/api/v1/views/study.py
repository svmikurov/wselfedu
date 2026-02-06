"""Word study API view."""

import logging
from http import HTTPStatus

from dependency_injector.wiring import Provide
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema,
)
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import di
from apps.core import views as core_views
from apps.core.api import renderers
from apps.lang.handlers import ApiPresentationUseCase
from apps.lang.repositories.abc import StudyParametersRepositoryABC
from apps.lang.services.exercise.abc import (
    WordProgressServiceABC,
)

from .. import examples
from .. import serializers as ser

log = logging.getLogger(__name__)

CONTAINER = di.MainContainer.lang.view_container.exercise  # type: ignore[attr-defined]


class WordStudyViewSet(
    core_views.UserRequestMixin,
    ViewSet,
):
    """Word study ViewSet."""

    renderer_classes = [renderers.WrappedJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    # -----------------------
    # Word study presentation
    # -----------------------

    @extend_schema(
        summary='Word study presentation',
        request=ser.WordParametersSerializer,
        responses={
            status.HTTP_200_OK: ser.WordStudyCaseSerializer,
        },
        examples=[
            OpenApiExample(
                'Request data example',
                value=examples.WORD_STUDY_PARAMETERS_DATA,
                request_only=True,
                status_codes=[HTTPStatus.OK],
            ),
        ],
        tags=['Lang'],
    )
    @action(methods=['post'], detail=False)
    def presentation(
        self,
        request: Request,
        service: ApiPresentationUseCase = Provide[
            CONTAINER.api_regular_presentation
        ],
    ) -> Response:
        """Render the Word study presentation case."""
        presentation = service.execute(self.user, request.data)
        return Response(presentation)

    # ---------------------
    # Word study parameters
    # ---------------------

    @extend_schema(
        summary='Word study parameters',
        responses={HTTPStatus.OK: ser.SetParametersSerializer},
        examples=[
            OpenApiExample(
                'Success response data example',
                value=examples.SET_WORD_STUDY_PARAMETERS_DATA,
                response_only=True,
                status_codes=[HTTPStatus.OK],
            ),
        ],
        tags=['Lang'],
    )
    @action(methods=['get'], detail=False)
    def parameters(
        self,
        request: Request,
        repository: StudyParametersRepositoryABC = Provide[
            CONTAINER.study_parameters_repository,
        ],
    ) -> Response:
        """Render initial Word study parameters."""
        payload = repository.fetch(self.request.user)  # type: ignore[arg-type]
        return Response(ser.SetParametersSerializer(payload).data)

    # ----------------------------
    # Update word study parameters
    # ----------------------------

    # TODO: Feat error handling for response
    @extend_schema(
        summary='Update word study parameters',
        request=ser.StudyParametersSerializer,
        tags=['Lang'],
    )
    @action(methods=['put'], detail=False, url_path='parameters/update')
    def update_parameters(
        self,
        request: Request,
        repository: StudyParametersRepositoryABC = Provide[
            CONTAINER.study_parameters_repository,
        ],
    ) -> Response:
        """Update initial Word study parameters."""
        params = ser.StudyParametersSerializer(data=request.data)
        params.is_valid()
        try:
            payload = repository.update(
                self.request.user,  # type: ignore[arg-type]
                params.validated_data,
            )
        except Exception as exc:
            log.exception('Update parameters error')
            return Response(
                data={'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(ser.SetParametersSerializer(payload).data)

    # --------------------------
    # Update word study progress
    # --------------------------

    # TODO: Add status codes with exceptions
    # TODO: Update response status to 200?
    @extend_schema(
        summary='Update word study progress',
        request=ser.WordStudyProgressSerializer,
        responses={},
        tags=['Lang'],
    )
    @action(methods=['post'], detail=False)
    def progress(
        self,
        request: Request,
        service: WordProgressServiceABC = Provide[
            CONTAINER.regular_translation_progress
        ],
    ) -> Response:
        """Update word study progress."""
        progress_serializer = ser.WordStudyProgressSerializer(
            data=request.data
        )

        if not progress_serializer.is_valid():
            log.warning(
                'Invalid progress data from user %s:\n%s.\nGot %s',
                request.user.id,
                progress_serializer.errors,
                request.data,
            )
            return Response(
                data=progress_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service.update_progress(
                request.user,  # type: ignore[arg-type]
                progress_serializer.validated_data,
            )
        except Exception as exc:
            log.exception('Update progress error')
            return Response(
                data={'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
