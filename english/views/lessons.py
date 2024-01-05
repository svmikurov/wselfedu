from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from english.forms import LessonForm
from english.models import LessonModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    UserPassesTestAdminMixin,
)

PAGINATE_NUMBER = 20


class LessonsListView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    ListView,
):
    model = LessonModel
    context_object_name = 'lessons'
    template_name = 'eng/lessons_list.html'
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Уроки',
    }


class LessonCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    CreateView,
):
    form_class = LessonForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:lessons_list')
    extra_context = {
        'title': 'Добавить урок',
        'btn_name': 'Добавить',
    }

    success_message = 'Урок добавлен'
    error_message = 'Ошибка в добавлении урока'


class LessonUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = LessonModel
    form_class = LessonForm
    template_name = 'form.html'
    success_url = reverse_lazy('eng:lessons_list')
    extra_context = {
        'title': 'Изменить урок',
        'btn_name': 'Изменить',
    }

    success_message = 'Урок изменен'
    error_message = 'Ошибка изменения урока'
    message_no_permission = 'Вы не можете этого делать'


class LessonDeleteView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    RedirectForModelObjectDeleteErrorMixin,
    AddMessageToFormSubmissionMixin,
    DeleteView,
):
    model = LessonModel
    template_name = 'delete.html'
    success_url = reverse_lazy('eng:lessons_list')
    extra_context = {
        'title': 'Удаление урока',
        'btn_name': 'Удалить',
    }
