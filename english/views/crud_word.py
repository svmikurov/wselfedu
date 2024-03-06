from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import WordModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    CheckOwnershipWordUserMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
)

CREATE_PATH = 'english:words_create'
LIST_PATH = 'english:word_list'

DETAIL_TEMPLATE = 'english/word_detail.html'
DELETE_TEMPLATE = 'delete.html'
FORM_TEMPLATE = 'english/word_form.html'
LIST_TEMPLATE = 'english/word_list.html'
USER_LIST_TEMPLATE = 'english/user_word_list.html'

PAGINATE_NUMBER = 20


class WordCreateView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessageToFormSubmissionMixin,
    CreateView,
):
    """Create word view."""

    form_class = WordForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(CREATE_PATH)
    success_message = 'Слово добавлено'

    additional_user_navigation = {
        'Словарь': LIST_TEMPLATE
    }
    extra_context = {
        'title': 'Добавить слово',
        'btn_name': 'Добавить',
        'additional_user_navigation': additional_user_navigation,
    }

    def form_valid(self, form):
        """Add current user to form."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class WordUpdateView(
    HandleNoPermissionMixin,
    CheckOwnershipWordUserMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    """Update word view."""

    model = WordModel
    form_class = WordForm
    template_name = FORM_TEMPLATE
    success_url = reverse_lazy(LIST_PATH)
    success_message = 'Слово изменено'
    context_object_name = 'word'
    extra_context = {
        'title': 'Изменить слово',
        'btn_name': 'Изменить',
    }


class WordDeleteView(
    HandleNoPermissionMixin,
    CheckOwnershipWordUserMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    """Delete word view."""

    model = WordModel
    template_name = DELETE_TEMPLATE
    success_url = reverse_lazy(LIST_PATH)
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }


class WordListView(
    HandleNoPermissionMixin,
    LoginRequiredMixin,
    AddMessageToFormSubmissionMixin,
    FilterView,
):
    """List word view."""

    model = WordModel
    filterset_class = WordsFilter
    template_name = LIST_TEMPLATE
    context_object_name = 'words'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Список слов',
    }

    def get_queryset(self):
        """Get word queryset to specific user."""
        queryset = super(WordListView, self).get_queryset(
        ).select_related(
            'category',
            'source',
        ).filter(
            user=self.request.user
        ).order_by(
            '-pk',
        )
        return queryset


class WordDetailView(
    HandleNoPermissionMixin,
    CheckOwnershipWordUserMixin,
    DetailView,
):
    """Delete word view."""

    model = WordModel
    template_name = DETAIL_TEMPLATE
    context_object_name = 'word'
    extra_context = {
        'title': 'Обзор слова',
    }
