"""Translation study settings views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from django.http.response import HttpResponse

from ... import forms, models


# TODO: Refactor
@login_required
def study_settings_view(request: HttpRequest) -> HttpResponse:
    """Render translation study parameters."""
    user = request.user
    parameters, _ = models.Parameters.objects.get_or_create(user=user)

    if request.method == 'POST':
        parameters_form = forms.ParametersForm(
            request.POST,
            instance=parameters,
        )
        translation_formset = forms.TranslationSettingsFormSet(
            request.POST,
            instance=user,  # type: ignore[arg-type]
            prefix='translation',
        )
        presentation_formset = forms.PresentationSettingsFormSet(
            request.POST,
            instance=user,  # type: ignore[arg-type]
            prefix='presentation',
        )

        all_valid = (
            parameters_form.is_valid()
            and translation_formset.is_valid()
            and presentation_formset.is_valid()
        )
        if all_valid:
            parameters_form.save()

            translation_result = translation_formset.save(commit=False)
            if not isinstance(translation_result, list):
                translation_result = [translation_result]

            for instance in translation_result:
                if instance:
                    instance.user = user  # type: ignore[assignment]
                    instance.save()

            presentation_result = presentation_formset.save(commit=False)
            if not isinstance(presentation_result, list):
                presentation_result = [presentation_result]

            for instance in presentation_result:  # type: ignore[assignment]
                if instance:
                    instance.user = user  # type: ignore[assignment]
                    instance.save()

            messages.success(request, 'Настройки успешно сохранены!')
            return redirect('lang:settings')

    else:
        parameters_form = forms.ParametersForm(
            instance=parameters,
        )
        translation_formset = forms.TranslationSettingsFormSet(
            instance=user,  # type: ignore[arg-type]
            prefix='translation',
        )
        presentation_formset = forms.PresentationSettingsFormSet(
            instance=user,  # type: ignore[arg-type]
            prefix='presentation',
        )

    context = {
        'parameters_form': parameters_form,
        'translation_formset': translation_formset,
        'presentation_formset': presentation_formset,
        'title': 'Настройки изучения',
        'header': 'Настройки изучения',
    }

    return render(request, 'lang/settings/index.html', context)
