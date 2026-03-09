"""Student's calculation exercises."""

from dependency_injector.wiring import Provide, inject
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from apps.core.adapters.response.shared import WebResponseDTO
from apps.core.handlers.dto import NullParams, RequestContext, RequestData
from apps.core.handlers.generic import RequestHandler
from apps.core.validators.request.null import NullValidated
from apps.core.views import UserLoginRequiredMixin
from apps.core.views.mixins import GetHandlerMixin
from apps.math.domains.dto import StudentExerciseDTO
from di import MainContainer

type StudentHandler = RequestHandler[
    NullParams,
    RequestContext,
    RequestData,
    NullValidated,
    list[StudentExerciseDTO],
    WebResponseDTO,
]

HANDLERS = MainContainer.math.exercise_web_views


class StudentCalculationExerciseListVew(
    UserLoginRequiredMixin,
    GetHandlerMixin[StudentHandler],
    TemplateView,
    View,
):
    """Student's calculation exercises."""

    template_name = 'math/exercise/calculation/student/index.html'

    @inject
    def dispatch(
        self,
        request: HttpRequest,
        *args: object,
        handler: StudentHandler = Provide[HANDLERS.student_exercises],  # type: ignore[attr-defined]
        **kwargs: object,
    ) -> HttpResponseBase:
        """Inject request handler."""
        self._handler = handler
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render student's exercises."""
        params = NullParams()
        request_context = RequestContext(user=self.user)
        data = RequestData(query=request.GET.dict())
        result = self.handler.execute(params, request_context, data)
        return render(request, self.get_template_names(), result.context)
