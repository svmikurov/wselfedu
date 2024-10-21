"""A module for user word assessment knowledge accounting.

Accounting of the level of knowledge of words in the application.

The module contains functions for querying the database for adding,
updating and retrieving the level of knowledge of words assessed by
the user.
The knowledge assessment has a limited range containing intervals.
Each interval is used by the selection of words for display on the
page of the user of the application.
Each user has his own assessments of words, given by him and available
only to him.
The application contains the following intervals: study, repetition,
verification, know.
"""

from config.constants import PROGRESS_MAX, PROGRESS_MIN, PROGRESS_STAGE_EDGES
from foreign.models import WordProgress


def get_progress(word_id: int, user_id: int) -> int:
    """Get or create a user rating of word knowledge.

    Get or create a user rating of word knowledge in the database.
    When creating a rating, the rating is set to "0".
    """
    if user_id and word_id:
        progress_obj, _ = WordProgress.objects.get_or_create(
            word_id=word_id,
            user_id=user_id,
        )
        progress = progress_obj.progress
        return progress


def update_progress(
    word_pk: int,
    user_pk: int,
    new_assessment: int,
) -> None:
    """Update the user's word knowledge score.

    Update the user's word knowledge score in the database, within the
    acceptable range.
    """
    if PROGRESS_MIN <= new_assessment <= PROGRESS_MAX:
        WordProgress.objects.filter(
            word_id=word_pk,
            user_id=user_pk,
        ).update(progress=new_assessment)


def get_numeric_value(progress: str) -> list[int]:
    """Convert a string representation of a knowledge level.

    Convert a string representation of a knowledge level into a range of
    numbers for that level.
    """
    value = []
    for assessment in PROGRESS_STAGE_EDGES:
        if assessment in progress:
            value += PROGRESS_STAGE_EDGES[assessment]
    return value
