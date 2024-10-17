"""CRUD Foreign words."""

from typing import Dict, Type

from crispy_forms.helper import FormHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.db.models import F, Q
from django.forms import Form
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from config.constants import (
    BTN_NAME,
    CATEGORY,
    CREATE_WORD_PATH,
    DELETE_TEMPLATE,
    DETAIL_WORD_TEMPLATE,
    FOREIGN_WORD,
    PAGINATE_NUMBER,
    PK,
    SOURCE,
    TITLE,
    USER,
    WORD,
    WORD_LIST_PATH,
    WORD_LIST_TEMPLATE,
    WORDS,
)
from contrib.views import (
    CheckUserOwnershipMixin,
    HandleNoPermissionMixin,
    PermissionProtectDeleteView,
    ReuseSchemaQueryFilterView,
)
from foreign.filters import WordsFilter
from foreign.forms import WordForm
from foreign.models import Word


class WordCreateView(HandleNoPermissionMixin, LoginRequiredMixin, CreateView):
    """Create word view."""

    form_class = WordForm
    template_name = 'foreign/word_add_form.html'
    success_url = reverse_lazy(CREATE_WORD_PATH)
    success_message = None

    additional_user_navigation = {'Словарь': WORD_LIST_TEMPLATE}
    extra_context = {
        TITLE: 'Добавить слово в словарь',
        'additional_user_navigation': additional_user_navigation,
    }

    def get_form(self, form_class: Type[Form] = None) -> FormHelper:
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = WordForm.apply_crispy_helper(form)
        return crispy_form

    def form_valid(self, form: Type[Form]) -> HttpResponse:
        """Add the current user to the form."""
        form.instance.user = self.request.user
        added_word = form.cleaned_data[FOREIGN_WORD]
        success_message = f'Добавлено слово "{added_word}"'
        WordCreateView.success_message = success_message
        form.save()
        response = super().form_valid(form)
        return response

    def render_to_response(
        self,
        context: Dict[str, object],
        **response_kwargs: object,
    ) -> JsonResponse | HttpResponse:
        """Return JsonResponse if `XMLHttpRequest` request."""
        is_ajax = (
            self.request.headers.get('X-requested-With') == 'XMLHttpRequest'
        )
        if is_ajax:
            return JsonResponse(
                data={'success_message': self.success_message},
                status=201,
            )
        else:
            return super(WordCreateView, self).render_to_response(
                context,
                **response_kwargs,
            )


class WordUpdateView(CheckUserOwnershipMixin, UpdateView):
    """Update word view."""

    model = Word
    form_class = WordForm
    template_name = 'foreign/word_form.html'
    success_url = reverse_lazy(WORD_LIST_PATH)
    success_message = 'Слово изменено'
    context_object_name = WORD
    extra_context = {
        TITLE: 'Изменить слово',
        BTN_NAME: 'Изменить',
    }

    def get_form(self, form_class: Type[Form] = None) -> FormHelper:
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = WordForm.apply_crispy_helper(form)
        return crispy_form


class WordDeleteView(PermissionProtectDeleteView):
    """Delete word view."""

    model = Word
    template_name = DELETE_TEMPLATE
    success_url = reverse_lazy(WORD_LIST_PATH)
    success_message = 'Слово удалено'
    extra_context = {
        TITLE: 'Удаление слова',
        BTN_NAME: 'Удалить',
    }


class WordListView(ReuseSchemaQueryFilterView):
    """Word list view."""

    model = Word
    filterset_class = WordsFilter
    template_name = WORD_LIST_TEMPLATE
    context_object_name = WORDS
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        TITLE: 'Список слов',
    }

    def get_queryset(self) -> models.query.QuerySet:
        """Get queryset to specific user."""
        user = self.request.user

        queryset = (
            super(WordListView, self)
            .get_queryset()
            .select_related(CATEGORY, SOURCE)
            .filter(user=user)
            .annotate(
                # Assign `True` if there is a relationship between
                # user and word in the wordfavorites, otherwise
                # assign None.
                favorites_anat=Q(
                    Q(wordfavorites__user=F(USER))
                    & Q(wordfavorites__word=F(PK))
                )
            )
            .annotate(assessment=F('wordprogress__progress'))
            .order_by('-pk')
        )
        return queryset


class WordDetailView(CheckUserOwnershipMixin, DetailView):
    """Detail word view."""

    model = Word
    template_name = DETAIL_WORD_TEMPLATE
    context_object_name = WORD
    extra_context = {
        TITLE: 'Обзор слова',
    }
