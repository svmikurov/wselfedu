"""English translation study views."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string

from apps.core.exceptions.info import NoTranslationsAvailableException

from .. import forms
from . import _data, base

if TYPE_CHECKING:
    from django.http.response import HttpResponse


class EnglishTranslationStudyView(base.SettingsBaseView):
    """English translation study view.

    Renders the study page with study settings data for case request.
    The page requests a new study case as partial template to update.
    """

    template_name = 'lang/study/index.html'
    extra_context = _data.ENGLISH_TRANSLATION['english_study']

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        """Add study settings to context."""
        context = super().get_context_data(**kwargs)
        context['study_setting'] = self.service.to_context(self.user)
        return context


# TODO: Fix type ignore, update messages.
# Add custom form view, without unused methods?
class EnglishTranslationStudyCaseView(base.CaseBaseView):
    """English translation study case view.

    Renders the partial template with new study case.
    """

    form_class = forms.CaseRequestForm
    """Validates case parameters and converts its to python dict.
    """

    def form_valid(self, form: forms.CaseRequestForm) -> HttpResponse:
        """If the case settings is valid, get and render the case."""
        try:
            case = self.service.get_case(self.user, form.cleaned_data)  # type: ignore[arg-type]
        except NoTranslationsAvailableException:
            messages.success(self.request, 'Нет переводов для изучения')
            return redirect('lang:settings')
        else:
            return self.render_partial(self.get_context_data(case=case))

    def form_invalid(self, form: forms.CaseRequestForm) -> HttpResponse:
        """Redirect to study settings if case request is invalid."""
        messages.success(self.request, 'Нет переводов для изучения')
        return redirect('lang:settings')

    def render_partial(self, context: dict[str, Any]) -> HttpResponse:
        """Return response with template for partial page update."""
        case_html = render_to_string('lang/study/_case.html', context)
        mark_html = render_to_string('lang/study/_mark_bar.html', context)
        combined_html = f'{case_html}\n{mark_html}'
        return HttpResponse(combined_html)
