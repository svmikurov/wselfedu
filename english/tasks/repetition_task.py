from random import choice
# from typing import Dict

from english.models import WordModel
from english.tasks.task_func import (
    get_random_sequence_language_keys,
)


def create_task(
        category_id: int,
        is_category_selected: bool,
        source_id,
) -> dict[str, str]:
    if is_category_selected:
        words: list[dict] = WordModel.objects.filter(
            category_id=category_id,
            source_id=source_id,
        ).values()
    else:
        words: list[dict] = WordModel.objects.filter(
            source_id=source_id,
        ).values()

    selected_word: dict = choice(words)
    question_key, answer_key = get_random_sequence_language_keys()

    question: str = selected_word.get(question_key)
    answer: str = selected_word.get(answer_key)
    task = {'question': question, 'answer': answer}

    return task
