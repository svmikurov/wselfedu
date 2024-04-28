from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from task.forms import WordChoiceForm
from english.services import create_lookup_params

from english.services.word_favorites import is_word_in_favorites
from english.services.word_knowledge_assessment import get_knowledge_assessment
from english.tasks.study_words import create_task

TITLE = {'title_name': 'Изучаем слова', 'url_name': 'task:word_choice'}


class WordChoiceView(TemplateView):
    # Add only for owner user
    """View choice English words to study."""

    template_name = 'task/word_choice.html'
    extra_context = {
        'title': TITLE,
    }

    def get_context_data(self, **kwargs):
        """Add a user-specific words form to context."""
        user_id = self.request.user.id
        context = super().get_context_data(**kwargs)
        context['form'] = WordChoiceForm(user_id=user_id)
        return context

    def post(self, request, *args, **kwargs):
        """Сохрани параметры фильтра слов для упражнения.

        Выполнит редирект на формирование задания и отображение вопроса.
        """
        user_id = request.user.id
        form = WordChoiceForm(request.POST, user_id=user_id)

        if form.is_valid():
            form_data = form.cleaned_data
            lookup_params = create_lookup_params(form_data, user_id)

            request.session['lookup_params'] = lookup_params
            request.session['language_order'] = form_data['language_order']
            request.session['timeout'] = form_data['timeout']

            return redirect(reverse_lazy('task:word_study_ajax'))
        else:
            return redirect(reverse_lazy('task:word_choice'))


class WordStudyView(View):
    """Представление для формирования задания и отображения вопроса."""

    template_name = 'task/word_study.html'

    def get(self, request, *args, **kwargs):
        """Создай задание и отобрази вопрос пользователю.
        """
        task = create_task(request)
        user_id = request.user.id
        word_id = task.get('word_id')
        knowledge = get_knowledge_assessment(word_id, user_id)
        favorites_status = is_word_in_favorites(user_id, word_id)

        context = {
            'title': TITLE,
            'task': task,
            'knowledge_assessment': knowledge,
            'favorites_status': favorites_status,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """Get new word task."""
        task = create_task(request)
        user_id = request.user.id
        word_id = task.get('word_id')
        knowledge = get_knowledge_assessment(word_id, user_id)
        favorites_status = is_word_in_favorites(user_id, word_id)

        return JsonResponse(
            data={
                'task': task,
                'knowledge_assessment': knowledge,
                'favorites_status': favorites_status,
            },
            status=200,
        )
