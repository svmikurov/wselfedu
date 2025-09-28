"""Word CRUD views."""

from dependency_injector.wiring import Provide
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from apps.users.models import CustomUser
from di import MainContainer

from ..forms import EnglishTranslationForm
from ..orchestrators import CreateEnglishTranslation


class EnglishTranslationCreateView(
    LoginRequiredMixin,
    FormView,  # type: ignore[type-arg]
):
    """View to create English word translation to leaning."""

    form_class = EnglishTranslationForm
    template_name = 'lang/translation_form.html'
    success_url = reverse_lazy('lang:translation_create')

    def form_valid(
        self,
        form: EnglishTranslationForm,
        orchestrator: CreateEnglishTranslation = Provide[
            MainContainer.lang.translation_orchestrator
        ],
    ) -> HttpResponse:
        """Save word translation."""
        if isinstance(self.request.user, CustomUser):
            orchestrator.create_translation(
                user=self.request.user,
                native=form.data['native'],
                english=form.data['english'],
            )
        return super().form_valid(form)
