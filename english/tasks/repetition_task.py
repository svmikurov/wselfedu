import logging
from random import choice

from english.models import WordModel, WordUserKnowledgeRelation
from english.tasks.task_func import (
    get_random_sequence_language_keys,
)
from users.models import UserModel

MAX_LEVEL_WORD_KNOWLEDGE_FOR_SHOW = 7

logging.basicConfig(level=logging.INFO)


def create_task(
        user_id: int,
        category_id: int,
        is_category_selected: bool,
        source_id,
) -> dict[str, str]:
    if is_category_selected:
        words = WordModel.objects.filter(
            category_id=category_id,
            source_id=source_id,
        )
    else:
        words = WordModel.objects.filter(
            source_id=source_id,
        )

    # Get user Queryset list word_id by user_id
    # which has not max level knowledge word.
    user_knowledge_words_pk = WordUserKnowledgeRelation.objects.filter(
        user=UserModel.objects.get(pk=user_id),
    ).filter(
        knowledge_assessment__lte=MAX_LEVEL_WORD_KNOWLEDGE_FOR_SHOW
    ).values_list('word_id', flat=True)

    # Get list WordModel instance of words for choice word.
    words_id_for_choice = []
    for word_bj in words:
        if word_bj.pk in user_knowledge_words_pk:
            words_id_for_choice.append(word_bj)

    # Choice random word for task.
    selected_word: dict = choice(words_id_for_choice)

    word_id = selected_word.pk
    question_key, answer_key = get_random_sequence_language_keys()

    task_word = {
        'words_eng': selected_word.words_eng,
        'words_rus': selected_word.words_rus,
    }
    question = task_word.get(question_key)
    answer = task_word.get(answer_key)
    task = {
        'word_id': word_id,
        'question': question,
        'answer': answer,
    }

    return task
