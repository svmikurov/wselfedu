"""Word study API view."""

import logging
import uuid

from dependency_injector import wiring
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import di
from apps.core.api import renderers
from apps.lang import types
from apps.lang.presenters.abc import WordStudyParamsPresenterABC
from apps.lang.services.abc import (
    WordPresentationServiceABC,
    WordProgressServiceABC,
)

from .. import serializers as ser

log = logging.getLogger(__name__)


class WordStudyViewSet(ViewSet):
    """Word study ViewSet."""

    renderer_classes = [renderers.WrappedJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Word study through the presentation',
        request={status.HTTP_200_OK: ser.WordStudySelectSerializer},
        responses={status.HTTP_200_OK: ser.WordStudyCaseSerializer},
        tags=['Lang'],
    )
    @action(methods=['post'], detail=False)
    def presentation(
        self,
        request: Request,
        presentation_services: WordPresentationServiceABC = wiring.Provide[
            di.MainContainer.lang.word_presentation_service,
        ],
    ) -> Response:
        """Render the word presentation."""
        study_params = ser.WordStudyParamsSerializer(data=request.data)
        study_params.is_valid(raise_exception=True)
        try:
            study_data = presentation_services.get_presentation_case(
                study_params.validated_data,
                self.request.user,  # type: ignore[arg-type]
            )
        except LookupError:
            return self._render_no_words()
        return Response(ser.WordStudyCaseSerializer(study_data).data)

    # TODO: Move to service
    def _render_no_words(self) -> Response:
        """Render no words to study for request params."""
        no_data: types.PresentationCase = {
            'case_uuid': uuid.uuid4(),
            'definition': '',
            'explanation': '',
            'info': {
                'progress': None,
            },
        }
        return Response(ser.WordStudyCaseSerializer(no_data).data)

    @extend_schema(
        summary='Word study params',
        responses=ser.WordStudySelectSerializer,
        tags=['Lang'],
    )
    @action(methods=['get'], detail=False)
    def params(
        self,
        request: Request,
        presenter: WordStudyParamsPresenterABC = wiring.Provide[
            di.MainContainer.lang.params_presenter,
        ],
    ) -> Response:
        """Render initial Word study params."""
        payload = presenter.get_initial(self.request.user)  # type: ignore[arg-type]
        return Response(ser.WordStudySelectSerializer(payload).data)

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
        service: WordProgressServiceABC = wiring.Provide[
            di.MainContainer.lang.progress_service,
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
            return Response(
                data={'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
