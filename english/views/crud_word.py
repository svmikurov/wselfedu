from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import WordModel
from contrib.mixins_views import (
    PermissionProtectDeleteView,
    ReuseSchemaQueryFilterView,
    CheckUserOwnershipMixin,
    HandleNoPermissionMixin,
)

CREATE_WORD_PATH = 'english:words_create'
WORD_LIST_PATH = 'english:word_list'

DELETE_WORD_TEMPLATE = 'delete.html'
DETAIL_WORD_TEMPLATE = 'english/word_detail.html'
WORD_LIST_TEMPLATE = 'english/word_list.html'

PAGINATE_NUMBER = 20


class WordCreateView(HandleNoPermissionMixin, LoginRequiredMixin, CreateView):
    """Create word view."""

    form_class = WordForm
    template_name = 'english/word_add_form.html'
    success_url = reverse_lazy(CREATE_WORD_PATH)
    success_message = None

    additional_user_navigation = {
        'Словарь': WORD_LIST_TEMPLATE
    }
    extra_context = {
        'title': 'Добавить слово в словарь',
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
        added_word = form.cleaned_data['word_eng']
        success_message = f'Добавлено слово "{added_word}"'
        setattr(WordCreateView, 'success_message', success_message)
        form.save()
        response = super().form_valid(form)
        return response

    def render_to_response(self, context, **response_kwargs):
        """Return JsonResponse if `XMLHttpRequest` request."""
        is_ajax = self.request \
                      .headers.get('X-requested-With') == 'XMLHttpRequest'
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

    model = WordModel
    form_class = WordForm
    template_name = 'english/word_form.html'
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


class WordDeleteView(PermissionProtectDeleteView):
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
            # Assign `True` if there is a relationship between user and
            # word in the WordsFavoritesModel, otherwise assign None.
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


class WordDetailView(CheckUserOwnershipMixin, DetailView):
    """Detail word view."""

    model = WordModel
    template_name = DETAIL_WORD_TEMPLATE
    context_object_name = 'word'
    extra_context = {
        'title': 'Обзор слова',
    }
