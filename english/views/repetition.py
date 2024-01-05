"""
Solution for repetition and learning of words.
Before the solution, you need to select a category and source of words.
First, the question word is displayed, then the translation is added to it.
Words are displayed in random order.
The language of the question word is also displayed in random order.
A timeout is set between displays.
The solution continues until it is interrupted.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from english.models import (
    CategoryModel,
    SourceModel,
    WordModel, WordUserKnowledgeRelation,
)
from english.tasks.repetition_task import create_task
from english.models.words import get_knowledge_assessment
from users.models import UserModel

TITLE = 'Переведи слова'
DEFAULT_CATEGORY = 'Все категории'
DEFAULT_CATEGORY_ID = 0
DEFAULT_SOURCE = 'Учебник'
DEFAULT_SOURCE_ID = 1
QUESTION_TIMEOUT = 7000  # ms
ANSWER_TIMEOUT = 7000  # ms
BTN_NAME = 'Начать'

INDEX_ERROR_MESSAGE = 'Ничего не найдено, попробуйте другие варианты'


class StartRepetitionWordsView(TemplateView):
    """
    Start solution.
    In this View is selected the category and source of repeated words.
    After this solution is redirected
    to another View in which it alternates words
    """
    categories = CategoryModel.objects.all()
    sources = SourceModel.objects.all()

    extra_context = {
        'title': TITLE,
        'categories': categories,
        'default_category': DEFAULT_CATEGORY,
        'default_category_id': DEFAULT_CATEGORY_ID,
        'sources': sources,
        'default_source': DEFAULT_SOURCE,
        'default_source_id': DEFAULT_SOURCE_ID,
        'task_status': 'question',
        'btn_name': BTN_NAME,
        'next_url': 'eng:repetition',
    }


class RepetitionWordsView(View):
    def get(self, request, *args, **kwargs):
        user_id = self.request.user.id
        task_status: str = kwargs.get('task_status')
        selected_category = request.GET.get('selected_category')
        selected_source = request.GET.get('selected_source')
        # selected_stage = request.GET.get('selected_stage')

        if selected_category:
            request.session['selected_category'] = selected_category
            request.session['selected_source'] = selected_source
        else:
            selected_category = request.session['selected_category']
            selected_source = request.session['selected_source']

        if task_status == 'question':
            try:
                task = create_task(
                    request,
                    selected_category,
                    selected_source,
                )
            except IndexError:
                messages.error(self.request, INDEX_ERROR_MESSAGE)
                return redirect(reverse_lazy('eng:start_repetition'))
            else:
                request.session['task'] = task
                timeout = QUESTION_TIMEOUT
        else:
            task = request.session['task']
            timeout = ANSWER_TIMEOUT

        word_id = task.get('word_id', '')

        # Get or create knowledge_assessment
        if request.user.is_authenticated:
            knowledge_assessment = get_knowledge_assessment(word_id, user_id)
        else:
            knowledge_assessment = 0

        context = {
            'title': TITLE,
            'task_status': task_status,
            'task': task,
            'timeout': timeout,
            'next_url': 'eng:repetition',
            'knowledge_assessment': knowledge_assessment,
            'word_id': word_id,
        }

        return render(request, 'eng/tasks/repetition.html', context)


@login_required
def knowledge_assessment_view(request, *args, **kwargs):
    """Изменяет в модели WordUserKnowledgeRelation значение поля
    knowledge_assessment (самооценки пользователя знания слова)
    """
    if request.user.is_authenticated:
        data = request.POST
        current_word_assessment = data['knowledge_assessment']
        word_pk = kwargs['word_id']
        user_pk = request.user.pk

        knowledge_assessment_obj, is_create = (
            WordUserKnowledgeRelation.objects.get_or_create(
                word=WordModel.objects.get(pk=word_pk),
                user=UserModel.objects.get(pk=user_pk),
            )
        )

        assessment = int(knowledge_assessment_obj.knowledge_assessment)
        assessment += int(current_word_assessment)
        knowledge_assessment_obj.knowledge_assessment = assessment
        knowledge_assessment_obj.save()

    return redirect(
        reverse_lazy(
            'eng:repetition',
            kwargs={'task_status': 'question'}
        )
    )
