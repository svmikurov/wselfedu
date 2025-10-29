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
from apps.lang import types
from apps.lang.presenters.abc import (
    WordStudyParamsPresenterABC,
    WordStudyPresenterABC,
)
from apps.users.models import CustomUser

from ..serializers import (
    WordStudyCaseSerializer,
    WordStudyParamsSelectSerializer,
    WordStudyParamsSerializer,
)


class WordStudyViewSet(ViewSet):
    """Word study ViewSet."""

    renderer_classes = [renderers.WrappedJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary='Word study through the presentation',
        request={status.HTTP_200_OK: WordStudyParamsSelectSerializer},
        responses={status.HTTP_200_OK: WordStudyCaseSerializer},
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
            return self._render_no_words()
        return Response(WordStudyCaseSerializer(study_data).data)

    def _render_no_words(self) -> Response:
        """Render no words to study for request params."""
        no_data: types.WordType = {
            'definition': '',
            'explanation': '',
        }
        return Response(WordStudyCaseSerializer(no_data).data)

    @extend_schema(
        summary='Word study params',
        responses=WordStudyParamsSelectSerializer,
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
        if not isinstance(self.request.user, CustomUser):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        payload = presenter.get_initial(self.request.user)
        return Response(WordStudyParamsSelectSerializer(payload).data)
