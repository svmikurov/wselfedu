"""Модуль задачи изучения пользователем слов.
"""

from random import shuffle

from django.contrib import messages
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy

from english.services.serve_query import (
    get_random_query_from_queryset,
    get_words_for_study,
)

MSG_NO_WORDS = 'Ничего не найдено, попробуйте другие варианты'
"""Нет слов, удовлетворяющих критериям выборки пользователя (`str`).
"""
RESTART_MSG = 'Выберите условия задания'
"""Сообщение о необходимости заново установить параметры выбора слова, в случае
ошибки приложения (`str`).
"""
CHOICE_PATH = 'english:word_choice'


def shuffle_sequence(sequence):
    """Перетасуй последовательность."""
    shuffle(sequence)
    return sequence


def get_language_order(word, order=None):
    """Return order of languages by user choice."""
    word_translations = [word.words_eng, word.words_rus]
    if order == 'EN':
        return word_translations
    elif order == 'RU':
        return [word.words_rus, word.words_eng]
    return shuffle_sequence(word_translations)


def get_google_link(word_eng):
    return (f'https://translate.google.com/?hl=ru&sl=auto&tl=ru&text='
            f'{word_eng}&op=translate')


def get_knowledge_action_url(word_id):
    return reverse_lazy(
        'english:knowledge_assessment',
        kwargs={'word_id': word_id},
    )


def create_task_study_words(
        *,
        lookup_params: dict,
        user_id: int,
        language_order=None,
) -> dict | None:
    """Create a task for the user to learn words using his filters.

    Parameters
    ----------
    lookup_params : `dict`
        Contains search options to select a word to display to the user.
    user_id : `int`
        Current user ID.
    language_order : `str` | None, optional
        User's choice of language order to display it to him.

    Arguments
    ---------
    word_count : `int`
        For display current word count at page as information.
    question : `str`
        Word to translate in the task.
    annswer : `str`
        Correct translation of the word.

    Returns
    -------
    task_study_word : `dict`
        Data for rendering context.
    """
    task_study_word = None
    word_qs: QuerySet = get_words_for_study(lookup_params, user_id)

    if word_qs:
        word_count = word_qs.count()
        word = get_random_query_from_queryset(word_qs)
        word_id = word.id
        question, answer = get_language_order(word, language_order)
        google_translate_word_link = get_google_link(word.words_eng)
        knowledge_action_url = get_knowledge_action_url(word_id)

        task_study_word = {
            'word_id': word_id,
            'question': question,
            'answer': answer,
            'word_eng': word.words_eng,
            'word_count': word_count,
            'source': word.source.name if word.source else '',
            'google_translate_word_link': google_translate_word_link,
            'knowledge_action_url': knowledge_action_url,
        }

    return task_study_word


def create_task(request):
    """"""
    user_id = request.user.id
    params_choice_url = reverse_lazy(CHOICE_PATH)

    try:
        lookup_params = request.session.get('lookup_params')
        language_order = request.session.get('language_order')
    except AttributeError:
        messages.error(request, RESTART_MSG)
        return redirect(params_choice_url)
    else:
        task = create_task_study_words(
            lookup_params=lookup_params,
            user_id=user_id,
            language_order=language_order,
        )

    if not task:
        messages.error(request, MSG_NO_WORDS)
        return redirect(params_choice_url)
    else:
        return task
