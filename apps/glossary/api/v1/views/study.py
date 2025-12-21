"""Terms study API view."""

from dependency_injector.wiring import Provide
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api.renderers import WrappedJSONRenderer
from apps.glossary.presenters.abc import TermStudyPresenterABC
from apps.users.models import Person
from di import MainContainer as Container

from ..serializers import (
    TermStudyParamsSerializer,
    TermStudyPresentationSerializer,
)


class TermStudyViewSet(viewsets.ViewSet):
    """Term study ViewSet."""

    renderer_classes = [WrappedJSONRenderer]

    @extend_schema(
        summary='Term study through the presentation',
        request={status.HTTP_200_OK: TermStudyParamsSerializer},
        responses={status.HTTP_200_OK: TermStudyPresentationSerializer},
        tags=['Glossary'],
    )
    @action(methods=['post'], detail=False)
    def presentation(
        self,
        request: Request,
        presenter: TermStudyPresenterABC = Provide[
            Container.glossary.term_study_presenter
        ],
    ) -> Response:
        """Render the Term presentation."""
        user = self.request.user
        if not isinstance(user, Person):
            return Response(status=status.HTTP_403_FORBIDDEN)

        study_params = TermStudyParamsSerializer(data=request.data)
        study_params.is_valid(raise_exception=True)
        study_data = presenter.get_case(user, study_params.data)
        return Response(TermStudyPresentationSerializer(study_data).data)
