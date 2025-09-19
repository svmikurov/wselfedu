"""Terms study API view."""

from dependency_injector.wiring import Provide
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from apps.core.api.renderers import WrappedJSONRenderer
from apps.glossary.presenters import TermsStudyPresenter
from di import MainContainer as Container

from ..serializers import (
    TermsStudyParamsSerializer,
    TermsStudyQuestionSerializer,
)


class TermsStudyViewSet(viewsets.ViewSet):
    """Term study viewset."""

    renderer_classes = [WrappedJSONRenderer]

    @action(methods=['post'], detail=False)
    def question(
        self,
        request: Request,
        exercise_prsenter: TermsStudyPresenter = Provide[
            Container.glossary.terms_study_presenter
        ],
    ) -> Response:
        """Get Terms study question."""
        exercise_params = TermsStudyParamsSerializer(data=request.data)
        exercise_params.is_valid(raise_exception=True)
        question = exercise_prsenter.get_question(exercise_params.data)
        return Response(TermsStudyQuestionSerializer(question).data)
