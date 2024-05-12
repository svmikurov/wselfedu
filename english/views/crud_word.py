from django.db.models import F, Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import WordModel
from contrib_app.mixins import (
    CheckLoginPermissionMixin,
    CheckObjectPermissionMixin,
    PermissionProtectDeleteView,
    ReuseSchemaQueryFilterView,
)

CREATE_WORD_PATH = 'english:words_create'
WORD_LIST_PATH = 'english:word_list'

DELETE_WORD_TEMPLATE = 'delete.html'
DETAIL_WORD_TEMPLATE = 'english/word_detail.html'
WORD_FORM_TEMPLATE = 'english/word_form.html'
WORD_LIST_TEMPLATE = 'english/word_list.html'

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

    def get_form(self, form_class=None):
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = WordForm.apply_crispy_helper(form)
        return crispy_form

    def form_valid(self, form):
        """Add the current user to the form."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class WordUpdateView(CheckObjectPermissionMixin, UpdateView):
    """Update word view."""

    model = WordModel
    form_class = WordForm
    template_name = WORD_FORM_TEMPLATE
    success_url = reverse_lazy(WORD_LIST_PATH)
    success_message = 'Слово изменено'
    context_object_name = 'word'
    extra_context = {
        'title': 'Изменить слово',
        'btn_name': 'Изменить',
    }

    def get_form(self, form_class=None):
        """Apply crispy form helper for form."""
        form = super().get_form()
        crispy_form = WordForm.apply_crispy_helper(form)
        return crispy_form


class WordDeleteView(CheckObjectPermissionMixin, PermissionProtectDeleteView):
    """Delete word view."""

    model = WordModel
    template_name = DELETE_WORD_TEMPLATE
    success_url = reverse_lazy(WORD_LIST_PATH)
    success_message = 'Слово удалено'
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }


class WordListView(ReuseSchemaQueryFilterView):
    """Word list view."""

    model = WordModel
    filterset_class = WordsFilter
    template_name = WORD_LIST_TEMPLATE
    context_object_name = 'words'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Список слов',
    }

    def get_queryset(self):
        """Get queryset to specific user."""
        user = self.request.user

        queryset = super(WordListView, self).get_queryset(
        ).select_related(
            'category',
            'source',
        ).filter(
            # Filter all words of a specific user.
            user=user
        ).annotate(
            # Assign `True` if there is a relationship between user and word
            # in the WordsFavoritesModel, otherwise assign `None`.
            favorites_anat=Q(
                Q(wordsfavoritesmodel__user=F('user'))
                & Q(wordsfavoritesmodel__word=F('pk'))
            )
        ).annotate(
            # Add to query `knowledge_assessment` value.
            assessment=F('worduserknowledgerelation__knowledge_assessment'),
        ).order_by(
            '-pk',
        )
        return queryset


class WordDetailView(CheckObjectPermissionMixin, DetailView):
    """Detail word view."""

    model = WordModel
    template_name = DETAIL_WORD_TEMPLATE
    context_object_name = 'word'
    extra_context = {
        'title': 'Обзор слова',
    }
