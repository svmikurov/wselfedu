"""English translation study view."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.wiring import Provide, inject
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from rest_framework.renderers import JSONRenderer

from apps.core.exceptions.info import NoTranslationsAvailableException
from apps.lang.api.v1 import serializers
from di import MainContainer

from . import _data, base

if TYPE_CHECKING:
    from django.http.request import HttpRequest

    from .. import services, types


class EnglishTranslationStudyView(base.SettingsBaseView):
    """English translation study view."""

    template_name = 'lang/study/index.html'
    extra_context = _data.ENGLISH_TRANSLATION['english_study']

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add study settings to context."""
        context = super().get_context_data(**kwargs)
        context['task'] = self.repository.get_task_settings(self.user)
        return context


# TODO: Fix type ignore
@inject
@login_required
def english_translation_case_htmx_view(
    request: HttpRequest,
    service: services.WordPresentationServiceABC = Provide[
        MainContainer.lang.word_presentation_service
    ],
) -> HttpResponse:
    """Render translation case as partial template for HTMX request."""
    parameters = request.GET.get('parameters', {})  # type: ignore[var-annotated]
    user = request.user

    try:
        case = service.get_presentation_case(user, parameters)  # type: ignore[arg-type]
    except NoTranslationsAvailableException:
        messages.success(request, 'Нет переводов для изучения')
        return redirect('lang:settings')

    context: dict[str, Any] = {
        **case,
        'task': {
            # TODO: Implement retrieve presentation settings form DB
            **_data.ENGLISH_TRANSLATION['english_study'],
            'known': to_progress_payload(case, True),
            'unknown': to_progress_payload(case, False),
        },
    }

    case_html = render_to_string('lang/study/_case.html', context)
    mark_html = render_to_string('lang/study/_mark_bar.html', context)

    combined_html = f'{case_html}\n{mark_html}'
    return HttpResponse(combined_html)


def to_progress_payload(
    case: types.CaseUUID, is_known: bool
) -> dict[str, str | bool]:
    """Build payload for study progress update request."""
    data = {'case_uuid': case['case_uuid'], 'is_known': is_known}
    serializer = serializers.WordStudyProgressSerializer(data=data)
    serializer.is_valid()
    return JSONRenderer().render(serializer.validated_data).decode('utf-8')  # type: ignore[no-any-return]
