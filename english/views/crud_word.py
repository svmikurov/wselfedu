from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django_filters.views import FilterView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import WordModel
from contrib_app.mixins import (
    CheckLoginPermissionMixin,
    CheckObjectPermissionMixin,
    PermissionProtectDeleteView,
)

CREATE_WORD_PATH = 'english:words_create'
LIST_WORD_PATH = 'english:word_list'

DELETE_WORD_TEMPLATE = 'delete.html'
DETAIL_WORD_TEMPLATE = 'english/word_detail.html'
WORD_FORM_TEMPLATE = 'english/word_form.html'
WORD_LIST_TEMPLATE = 'english/word_list.html'
USER_WORD_LIST_TEMPLATE = 'english/user_word_list.html'

PAGINATE_NUMBER = 20


class WordCreateView(CheckLoginPermissionMixin, CreateView):
    """Create word view."""

    form_class = WordForm
    template_name = WORD_FORM_TEMPLATE
    success_url = reverse_lazy(CREATE_WORD_PATH)
    success_message = 'Слово добавлено'

    additional_user_navigation = {
        'Словарь': WORD_LIST_TEMPLATE
    }
    extra_context = {
        'title': 'Добавить слово',
        'btn_name': 'Добавить',
        'additional_user_navigation': additional_user_navigation,
    }

    def form_valid(self, form):
        """Add current user to form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class WordUpdateView(CheckObjectPermissionMixin, UpdateView):
    """Update word view."""

    model = WordModel
    form_class = WordForm
    template_name = WORD_FORM_TEMPLATE
    success_url = reverse_lazy(LIST_WORD_PATH)
    success_message = 'Слово изменено'
    context_object_name = 'word'
    extra_context = {
        'title': 'Изменить слово',
        'btn_name': 'Изменить',
    }


class WordDeleteView(CheckObjectPermissionMixin, PermissionProtectDeleteView):
    """Delete word view."""

    model = WordModel
    template_name = DELETE_WORD_TEMPLATE
    success_url = reverse_lazy(LIST_WORD_PATH)
    success_message = 'Слово удалено'
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }


class WordListView(CheckLoginPermissionMixin, FilterView):
    """List word view."""

    model = WordModel
    filterset_class = WordsFilter
    template_name = WORD_LIST_TEMPLATE
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


class WordDetailView(CheckObjectPermissionMixin, DetailView):
    """Delete word view."""

    model = WordModel
    template_name = DETAIL_WORD_TEMPLATE
    context_object_name = 'word'
    extra_context = {
        'title': 'Обзор слова',
    }
