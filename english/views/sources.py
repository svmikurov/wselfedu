from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from english.forms.source import SourceForm
from english.models import SourceModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    UserPassesTestAdminMixin,
)

PAGINATE_NUMBER = 20


class SourceListView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    ListView,
):
    model = SourceModel
    context_object_name = 'sources'
    template_name = 'eng/sources_list.html'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Источники для изучения слов',
    }


class SourceCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    CreateView,
):
    form_class = SourceForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:sources_list')
    extra_context = {
        'title': 'Добавить источник слов',
        'btn_name': 'Добавить',
    }

    success_message = 'Источник слов успешно добавлен'
    error_message = 'Ошибка в добавлении источника слов'


class SourceUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = SourceModel
    form_class = SourceForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:sources_list')
    extra_context = {
        'title': 'Изменить источник слов',
        'btn_name': 'Изменить',
    }

    success_message = 'Источник слов успешно изменен'
    error_message = 'Ошибка изменения источника слов'
    message_no_permission = 'Вы не можете этого делать'


class SourceDeleteView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    model = SourceModel
    template_name = 'delete.html'
    success_url = reverse_lazy('eng:sources_list')
    extra_context = {
        'title': 'Удаление источника слов',
        'btn_name': 'Удалить',
    }
