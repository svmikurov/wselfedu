from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView, DetailView,
)
from django_filters.views import FilterView

from english.filters import WordsFilter
from english.forms import WordForm
from english.models import WordModel, CategoryModel
from contrib_app.mixins import (
    AddMessageToFormSubmissionMixin,
    HandleNoPermissionMixin,
    RedirectForModelObjectDeleteErrorMixin,
    UserPassesTestAdminMixin,
)

PAGINATE_NUMBER = 20


class WordListView(
    FilterView,
):
    """View a word list page."""

    template_name = 'english/word_list.html'
    model = WordModel
    context_object_name = 'words'
    filterset_class = WordsFilter
    paginate_by = PAGINATE_NUMBER
    extra_context = {'title': 'Список слов'}


class WordCreateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    CreateView,
):
    form_class = WordForm
    template_name = 'form.html'
    success_url = reverse_lazy('english:words_create')

    additional_user_navigation = {
        'Словарь': 'english:word_list'
    }
    extra_context = {
        'title': 'Добавить слово',
        'btn_name': 'Добавить',
        'additional_user_navigation': additional_user_navigation,
    }

    success_message = 'Слово успешно добавлено'
    error_message = 'Ошибка в добавлении слова'

    default_category_name = 'category3'

    def form_valid(self, form):
        """Add current user and category instance default to model.

        If form don't contain category instance, set category instance by
        default "category3".
        """
        form.instance.user = self.request.user
        if not form.instance.category:
            form.instance.category = CategoryModel.objects.get(
                name=self.default_category_name
            )
        return super().form_valid(form)


class WordDetailView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    DetailView,
):
    model = WordModel
    template_name = 'english/word_detail.html'
    context_object_name = 'word'


class WordUpdateView(
    HandleNoPermissionMixin,
    UserPassesTestAdminMixin,
    AddMessageToFormSubmissionMixin,
    UpdateView,
):
    model = WordModel
    form_class = WordForm
    template_name = 'form.html'
    success_url = reverse_lazy('english:word_list')
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
    success_url = reverse_lazy('english:word_list')
    extra_context = {
        'title': 'Удаление слова',
        'btn_name': 'Удалить',
    }


class ShowUsersWordsView(FilterView):
    model = WordModel
    template_name = 'english/user_word_list.html'
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
