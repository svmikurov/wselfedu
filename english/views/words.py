# from typing import Type

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import WordModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    UserPassesTestAdminMixin,
)

SUPERTITLE = 'Английский язык'
LIST_ITEMS = {
    'name': 'Список слов',
    'href': 'eng:words_list',
}
PAGINATE_NUMBER = 20


class WordListView(
    FilterView,
):
    template_name = 'eng/words_list.html'
    model = WordModel
    context_object_name = 'words'
    filterset_class = WordsFilter
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Список слов',
    }


class WordCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    CreateView,
):
    form_class = WordForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:word_create')
    extra_context = {
        'title': 'Добавить слово',
        'btn_name': 'Добавить',
        'list_items': LIST_ITEMS,
    }

    success_message = 'Слово успешно добавлено'
    error_message = 'Ошибка в добавлении слова'
    # message_no_permission = 'К сожалению, вы пока не можете добавить слово'

    def form_valid(self, form):
        """Add current user to model"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class WordUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = WordModel
    form_class = WordForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:words_list')
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
    template_name = 'delete.html'
    success_url = reverse_lazy('eng:words_list')
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }
