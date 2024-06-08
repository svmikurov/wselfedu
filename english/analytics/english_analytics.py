from django.db.models import F

from english.models import WordLearningStories, WordModel


def collect_statistics(task) -> None:
    """Add word display to statistics.

    Added word display to :model:`english.WordLearningStories` in
    `display_count` fild.
    """
    word_id = task.word_id
    even, _ = WordLearningStories.objects.get_or_create(
        word=WordModel.objects.get(id=word_id)
    )
    even.display_count = F('display_count') + 1
    even.save()
