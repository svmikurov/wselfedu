from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from english.forms.source import SourceForm
from english.models import SourceModel
from contrib_app.mixins import (
    CheckLoginPermissionMixin,
    CheckObjectPermissionMixin,
    PermissionProtectDeleteView,
)

SOURCE_LIST_PATH = 'english:sources_list'

DELETE_SOURCE_TEMPLATE = 'delete.html'
SOURCE_FORM_TEMPLATE = 'form.html'
SOURCE_LIST_TEMPLATE = 'english/sources_list.html'

PAGINATE_NUMBER = 20


class SourceCreateView(CheckLoginPermissionMixin, CreateView):
    """Create source view."""

    form_class = SourceForm
    template_name = SOURCE_FORM_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов добавлен'
    extra_context = {
        'title': 'Добавить источник слов',
        'btn_name': 'Добавить',
    }

    def form_valid(self, form):
        """Add the logged-in user to the `user` field of the SourceModel."""
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class SourceUpdateView(CheckObjectPermissionMixin, UpdateView):
    """Update source view."""

    model = SourceModel
    form_class = SourceForm
    template_name = SOURCE_FORM_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов изменен'
    extra_context = {
        'title': 'Изменить источник слов',
        'btn_name': 'Изменить',
    }


class SourceDeleteView(PermissionProtectDeleteView):
    """Delete source view."""

    model = SourceModel
    template_name = DELETE_SOURCE_TEMPLATE
    success_url = reverse_lazy(SOURCE_LIST_PATH)
    success_message = 'Источник слов удален'
    protected_redirect_url = reverse_lazy(SOURCE_LIST_PATH)
    protected_message = ('Невозможно удалить этот объект, так как он '
                         'используется в другом месте приложения')
    extra_context = {
        'title': 'Удаление источника слов',
        'btn_name': 'Удалить',
    }


class SourceListView(CheckLoginPermissionMixin, ListView):
    """List source view."""

    model = SourceModel
    context_object_name = 'sources'
    template_name = SOURCE_LIST_TEMPLATE
    paginate_by = PAGINATE_NUMBER
    extra_context = {
        'title': 'Источники для изучения слов',
    }

    def get_queryset(self):
        queryset = super().get_queryset(
        ).filter(
            user=self.request.user.id
        )
        return queryset
