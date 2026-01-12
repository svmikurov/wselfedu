"""Rule example/exception views."""

from typing import Any

from django.views import generic
from django.shortcuts import get_object_or_404
from django.forms import BaseForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

from apps.core.views.auth import UserRequestMixin
from apps.lang import forms, models


class ClauseExampleView(UserRequestMixin, generic.FormView):  # type: ignore[type-arg]
    """Rule example view."""

    template_name = 'lang/rule/detail/_form.html'
    form_class = forms.ClauseTranslationForm

    def get_form_kwargs(self) -> dict[str, Any]:
        """Add data to form."""
        kwargs = super().get_form_kwargs()
        
        rule = get_object_or_404(
            models.Rule,
            pk=self.kwargs['pk'],
            user=self.user,
        )

        kwargs['user'] = self.user
        kwargs['rule'] = rule
        return kwargs

    def form_valid(self, form: BaseForm) -> HttpResponse:
        """Handle valid form submission."""
        try:
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            return self.form_invalid(form)

    def get_success_url(self) -> str:
        """Return URL to redirect after successful form submission."""
        return reverse('lang:english_rule_detail', kwargs={'pk': self.kwargs['pk']})


class RuleExceptionView(generic.TemplateView):
    """Rule example view."""
