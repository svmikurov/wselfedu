"""Word translation CRUD views."""

from dependency_injector.wiring import Provide
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from apps.users.models import CustomUser
from di import MainContainer

from ..forms import EnglishTranslationForm
from ..models import EnglishTranslation
from ..presenters import EnglishTranslationPresenter, TranslationParams
from ..repos import TranslationRepo


class EnglishTranslationCreateView(
    LoginRequiredMixin,
    generic.FormView,  # type: ignore[type-arg]
):
    """View to create English word translation to leaning."""

    form_class = EnglishTranslationForm
    template_name = 'lang/translation_form.html'
    success_url = reverse_lazy('lang:translation_english_create')

    def form_valid(
        self,
        form: EnglishTranslationForm,
        repo: TranslationRepo = Provide[MainContainer.lang.translation_repo],
    ) -> HttpResponse:
        """Save word translation."""
        repo.create_translation(
            user=self.request.user,  # type: ignore[arg-type]
            native=form.data['native'],
            english=form.data['english'],
        )
        return super().form_valid(form)


class EnglishTranslationListView(
    LoginRequiredMixin,
    generic.ListView,  # type: ignore[type-arg]
):
    """View to render the English word translations list."""

    template_name = 'lang/translation_english_list.html'
    context_object_name = 'translations'

    def get_queryset(self) -> QuerySet[EnglishTranslation]:
        """Get English word translations queryset."""
        params = self._get_params()
        query = self._get_presenter().get_translations(params=params)
        return query

    @staticmethod
    def _get_presenter(
        presenter: EnglishTranslationPresenter = Provide[
            MainContainer.lang.translation_presenter
        ],
    ) -> EnglishTranslationPresenter:
        """Get English word translations presenter."""
        return presenter

    def _get_params(self) -> TranslationParams | None:
        """Get translation filter params."""
        if isinstance(self.request.user, CustomUser):
            return TranslationParams(
                user=self.request.user,
                labels=None,
            )
        return None
