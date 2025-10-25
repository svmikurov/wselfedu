"""Word study API view."""

from dependency_injector import wiring
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

import di
from apps.core.api import renderers
from apps.lang.presenters.abc import WordStudyPresenterABC

from ..serializers.word_study import (
    WordStudyParamsSerializer,
    WordStudyPresentationsSerializer,
)


class WordStudyViewSet(ViewSet):
    """Word study ViewSet."""

    renderer_classes = [renderers.WrappedJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Word study through the presentation',
        request={status.HTTP_200_OK: WordStudyParamsSerializer},
        responses={status.HTTP_200_OK: WordStudyPresentationsSerializer},
        tags=['Lang'],
    )
    @action(methods=['post'], detail=False)
    def presentation(
        self,
        request: Request,
        presenter: WordStudyPresenterABC = wiring.Provide[
            di.MainContainer.lang.word_study_presenter,
        ],
    ) -> Response:
        """Render the word presentation."""
        study_params = WordStudyParamsSerializer(data=request.data)
        study_params.is_valid(raise_exception=True)
        try:
            study_data = presenter.get_presentation(
                study_params.validated_data,
                self.request.user,  # type: ignore[arg-type]
            )
        except LookupError:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(WordStudyPresentationsSerializer(study_data).data)
