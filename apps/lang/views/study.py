"""English translation study view."""

from dependency_injector.wiring import Provide, inject
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import (
    HttpResponse,
)
from django.template.loader import render_to_string
from django.views import generic

from di import MainContainer

from .. import services
from . import context


class EnglishTranslationStudyView(generic.TemplateView):
    """English translation study view."""

    template_name = 'lang/translation_study.html'
    extra_context = context.ENGLISH_TRANSLATION['english_study']


# TODO: Fix type ignore
# TODO: Implement retrieval of presentation user settings from database
@inject
@login_required
def english_translation_case_htmx_view(
    request: HttpRequest,
    service: services.WordPresentationService = Provide[
        MainContainer.lang.word_presentation_service
    ],
) -> HttpResponse:
    """Render translation case as partial template for HTMX request."""
    parameters = request.GET.get('parameters', {})  # type: ignore[var-annotated]
    user = request.user

    case = service.get_presentation_case(user, parameters)  # type: ignore[arg-type]

    html = render_to_string(
        template_name='lang/presentation/partial.html',
        context={
            **case,
            'task': {
                'url': '/lang/translation/english/study/case/',
                'presentation_timeout': 4000,
                'answer_timeout': 2000,
            },
        },
    )
    return HttpResponse(html)
