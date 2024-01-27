from django.contrib.auth.mixins import LoginRequiredMixin
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
    LoginRequiredMixin,
    ListView,
):
    model = SourceModel
    context_object_name = 'sources'
    template_name = 'english/sources_list.html'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Источники для изучения слов',
    }
    message_no_permission = 'Вы пока не можете делать это'


class SourceCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    CreateView,
):
    form_class = SourceForm
    template_name = 'form.html'
    success_url = reverse_lazy('english:sources_list')
    extra_context = {
        'title': 'Добавить источник слов',
        'btn_name': 'Добавить',
    }

    success_message = 'Источник слов добавлен'
    error_message = 'Ошибка в добавлении источника слов'
    message_no_permission = 'Вы пока не можете делать это'


class SourceUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = SourceModel
    form_class = SourceForm
    template_name = 'form.html'
    success_url = reverse_lazy('english:sources_list')
    extra_context = {
        'title': 'Изменить источник слов',
        'btn_name': 'Изменить',
    }

    success_message = 'Источник слов изменен'
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
    success_url = reverse_lazy('english:sources_list')
    extra_context = {
        'title': 'Удаление источника слов',
        'btn_name': 'Удалить',
    }
    success_message = 'Источник слов удален'
    protected_redirect_url = reverse_lazy('english:sources_list')
    protected_message = (
        'Невозможно удалить этот объект, '
        'так как он используется в другом месте приложения'
    )
