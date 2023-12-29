from random import shuffle

from django.contrib.auth import get_user_model

User = get_user_model()


def get_random_sequence_language_keys() -> list[str]:
    """Return a random sequence of language keys."""
    language_keys = ['words_eng', 'words_rus']
    shuffle(language_keys)
    return language_keys
