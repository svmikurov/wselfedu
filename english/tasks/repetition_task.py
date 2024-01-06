from random import choice

from config.logger_config import logger
from english.tasks.task_func import (
    get_random_sequence_language_keys,
)

MAX_LEVEL_WORD_KNOWLEDGE_FOR_SHOW = 4


def add_filers_to_queryset(request, words_qs):
    """Добавь фильтры в QuerySet."""
    # Получи словарь фильтров из сессии, если он там есть.
    # Создай пустой словарь фильтров, если его нет в сессии.
    words_filter = request.session.get('words_filter', dict())

    # Получи из GET запроса значения для фильтрации по категории и источнику.
    # Если они сеть, то обнови словарь фильтров.
    category_id = request.GET.get('category_id')
    if category_id:
        words_filter['category_id'] = category_id
    source_id = request.GET.get('source_id')
    if source_id:
        words_filter['source_id'] = source_id

    # Если есть значения фильтров в словаре, примени их последовательно к
    # QuerySet.
    category_id = words_filter.get('category_id')
    if category_id:
        words_qs = words_qs.filter(category_id=category_id)
        logger.debug(f'Произведена фильтрация по category_id = {category_id}')
    source_id = words_filter.get('source_id')
    if source_id:
        words_qs = words_qs.filter(source_id=source_id)
        logger.debug(f'Произведена фильтрация по source_id = {source_id}')

    # Обнови словарь фильтров в сессии.
    if words_filter:
        request.session['words_filter'] = words_filter
        logger.debug('Обновлен словарь в сессии')

    return words_qs.values()


def create_task(words: list[dict]) -> dict[str, str]:
    selected_word: dict = choice(words)
    question_key, answer_key = get_random_sequence_language_keys()

    task_word = {
        'words_eng': selected_word.get('words_eng'),
        'words_rus': selected_word.get('words_rus'),
    }
    task = {
        'word_id': selected_word.get('id'),
        'question': task_word.get(question_key),
        'answer': task_word.get(answer_key),
    }
    return task
