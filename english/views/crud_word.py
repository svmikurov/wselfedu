from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django_filters.views import FilterView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import CategoryModel, WordModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    UserPassesTestAdminMixin,
)

LIST_WORD_PATH_NAME = 'english:word_list'
CREATE_WORD_PATH_NAME = 'english:words_create'

LIST_WORD_TEMPLATE_NAME = 'english/word_list.html'
USER_LIST_WORD_TEMPLATE_NAME = 'english/user_word_list.html'
FORM_WORD_TEMPLATE_NAME = 'english/word_form.html'
DETAIL_WORD_TEMPLATE_NAME = 'english/word_detail.html'
DELETE_WORD_TEMPLATE_NAME = 'delete.html'

DEFAULT_WORD_CATEGORY = 'Developer'
"""Константа значения добавления категории по умолчанию, если пользователем не
не указана категория.
"""
PAGINATE_NUMBER = 20


class WordListView(
    FilterView,
):
    """View a word list page."""

    template_name = LIST_WORD_TEMPLATE_NAME
    model = WordModel
    context_object_name = 'words'
    filterset_class = WordsFilter
    paginate_by = PAGINATE_NUMBER
    extra_context = {'title': 'Список слов'}

    def get_queryset(self):
        queryset = super(WordListView, self).get_queryset(
        ).select_related(
            'category',
            'source',
        ).order_by('-pk')
        return queryset


class WordCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    CreateView,
):
    form_class = WordForm
    template_name = FORM_WORD_TEMPLATE_NAME
    success_url = reverse_lazy(CREATE_WORD_PATH_NAME)

    additional_user_navigation = {
        'Словарь': LIST_WORD_TEMPLATE_NAME
    }
    extra_context = {
        'title': 'Добавить слово',
        'btn_name': 'Добавить',
        'additional_user_navigation': additional_user_navigation,
    }

    success_message = 'Слово успешно добавлено'
    error_message = 'Ошибка в добавлении слова'

    def form_valid(self, form):
        """Add current user and category instance default to model.

        If form don't contain category instance, set category instance by
        default "category3".
        """
        form.instance.user = self.request.user
        if not form.instance.category:
            form.instance.category = CategoryModel.objects.get(
                name=DEFAULT_WORD_CATEGORY
            )
        return super().form_valid(form)


class WordDetailView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    DetailView,
):
    model = WordModel
    template_name = DETAIL_WORD_TEMPLATE_NAME
    context_object_name = 'word'
    extra_context = {
        'title': 'Обзор слова',
    }


class WordUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = WordModel
    form_class = WordForm
    template_name = FORM_WORD_TEMPLATE_NAME
    success_url = reverse_lazy(LIST_WORD_PATH_NAME)
    context_object_name = 'word'
    extra_context = {
        'title': 'Изменить слово',
        'btn_name': 'Изменить',
    }

    success_message = 'Слово успешно изменено'
    error_message = 'Ошибка изменения слова'
    message_no_permission = 'Вы не можете этого делать'


class WordDeleteView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    model = WordModel
    template_name = DELETE_WORD_TEMPLATE_NAME
    success_url = reverse_lazy(LIST_WORD_PATH_NAME)
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }


class ShowUsersWordsView(FilterView):
    model = WordModel
    template_name = USER_LIST_WORD_TEMPLATE_NAME
    paginate_by = PAGINATE_NUMBER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        words = WordModel.objects.all().select_related(
            'user',
            'source',
            'category',
            'lesson',
        )
        context['words'] = words
        return context
