"""English translation study views."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from django.contrib import messages
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse

from apps.core.exceptions.info import NoTranslationsAvailableException

from . import _data, base


class EnglishTranslationStudyView(base.SettingsBaseView):
    """English translation study view.

    Renders the study page with study settings data for case request.
    The page requests a new study case as partial template to update.
    """

    template_name = 'lang/presentation/index.html'
    extra_context = _data.ENGLISH_TRANSLATION['english_study']

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add study settings to context."""
        context = super().get_context_data(**kwargs)
        context['study_setting'] = self.service.to_context(self.user)
        return context


class EnglishTranslationStudyCaseView(base.CaseBaseView):
    """English translation study case view."""

    def post(self, request: HttpRequest) -> HttpResponse:
        """If the case settings is valid, get and render the case."""
        try:
            case = self.use_case.execute(self.user, self.request.POST.dict())

        except NoTranslationsAvailableException:
            messages.success(self.request, 'Нет переводов для изучения')
            return self.handle_no_presentation_case()

        return self.render_partial(self.get_context_data(case=case))

    def render_partial(self, context: dict[str, Any]) -> HttpResponse:
        """Return response with template for partial page update."""
        case = render_to_string('lang/presentation/_case.html', context)
        mark = render_to_string('lang/presentation/_mark_bar.html', context)
        combined_html = f'{case}\n{mark}'
        return HttpResponse(combined_html)

    def handle_no_presentation_case(self) -> JsonResponse:
        """Render json response if no presentation case."""
        return JsonResponse(
            data={
                'status': 'error',
                'message': 'No presentation case',
                'next': reverse('lang:settings'),
            },
            status=HTTPStatus.OK,
        )
