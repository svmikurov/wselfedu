"""Exercise and exercise params database queries."""

from django.contrib.auth.base_user import AbstractBaseUser

from foreign.models import (
    TranslateParams,
    WordCategory,
    WordSource,
)


def save_params(user: AbstractBaseUser, task_conditions: dict) -> None:
    """Save user exercise params to database."""
    params, _ = TranslateParams.objects.get_or_create(user=user)
    params.favorites = task_conditions['favorites']
    params.order = task_conditions['order']
    params.period_start_date = task_conditions['period_start_date']
    params.period_end_date = task_conditions['period_end_date']
    params.word_count = task_conditions['word_count']
    params.progress = task_conditions['progress']
    params.timeout = task_conditions['timeout']

    category_id = task_conditions['category']
    if category_id:
        params.category = WordCategory.objects.get(pk=category_id)
    else:
        params.category = None

    source_id = task_conditions['source']
    if source_id:
        params.source = WordSource.objects.get(pk=source_id)
    else:
        params.source = None

    params.save()
