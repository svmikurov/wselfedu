from random import sample, randint

from django.contrib.auth import get_user_model

from english.models import (
    WordModel,
)
from english.tasks.repetition_task import get_random_sequence_language_keys

User = get_user_model()

COUNT_OF_WORDS = 5


class TestWordTask:
    words = WordModel.objects.all()

    def get_random_words_for_task(self):
        """
        Return a list of random words
        """
        words = self.words.values()
        word_count = len(words)
        random_indexes = sample(range(word_count), k=COUNT_OF_WORDS)

        words_for_task = []
        for index in random_indexes:
            words_for_task.append(words[index])

        return words_for_task

    def get_random_word_for_task(self, words_for_choice):
        """
        Return a random task word from list of random words
        """
        random_word_task_index: int = randint(0, COUNT_OF_WORDS - 1)
        return words_for_choice[random_word_task_index]

    def create_task(self):
        """
        Return random task
        Return random choices answer
        """
        words_for_choice = self.get_random_words_for_task()
        task_language, answer_language = get_random_sequence_language_keys()

        task_words = []
        for word in words_for_choice:
            task_words.append(
                {
                    'id': word.get('id'),
                    'task_word': word.get(task_language),
                    'answer_word': word.get(answer_language),
                }
            )

        random_word = self.get_random_word_for_task(task_words)

        return random_word, task_words
