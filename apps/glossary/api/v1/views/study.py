"""Terms study API view."""

from dependency_injector.wiring import Provide
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api.renderers import WrappedJSONRenderer
from apps.glossary.presenters import TermStudyPresenter
from di import MainContainer as Container

from ..serializers import (
    TermStudyParamsSerializer,
    TermStudyPresentationSerializer,
)


class TermStudyViewSet(viewsets.ViewSet):
    """Term study viewset."""

    renderer_classes = [WrappedJSONRenderer]

    @extend_schema(
        summary='Term study through the presentation',
        tags=['Glossary'],
    )
    @action(methods=['post'], detail=False)
    def presentation(
        self,
        request: Request,
        prsenter: TermStudyPresenter = Provide[
            Container.glossary.term_study_presenter
        ],
    ) -> Response:
        """Render the Term prsentanion."""
        study_params = TermStudyParamsSerializer(data=request.data)
        study_params.is_valid(raise_exception=True)
        study_data = prsenter.get_presentation(study_params.data)
        return Response(TermStudyPresentationSerializer(study_data).data)
