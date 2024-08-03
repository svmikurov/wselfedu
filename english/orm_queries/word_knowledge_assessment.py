"""A module for user assessment and accounting of the level of
knowledge of words in the application.

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

from english.models import WordUserKnowledgeRelation

MIN_KNOWLEDGE_ASSESSMENT = 0
MAX_STUDYING_VALUE = 6
MAX_REPETITION_VALUE = 8
MAX_EXAMINATION_VALUE = 10
MAX_KNOWLEDGE_ASSESSMENT = 11
"""Значения оценки уровня знания слова пользователем
"""
WORD_STUDY_ASSESSMENTS = {
    'S': [*range(MIN_KNOWLEDGE_ASSESSMENT, MAX_STUDYING_VALUE + 1)],
    'R': [*range(MAX_STUDYING_VALUE + 1, MAX_REPETITION_VALUE + 1)],
    'E': [*range(MAX_REPETITION_VALUE + 1, MAX_EXAMINATION_VALUE + 1)],
    'K': [MAX_KNOWLEDGE_ASSESSMENT],
}
"""A literal representation of an knowledge assessment
(`dict[str, list[int]]`).

key : `str`
    A literal representation of an knowledge assessment.
    Where:
        'S' - is a word in the process of studied;
        'R' - word in process of repetition;
        'E' - is a word in the process of examination;
        'K' - the word has been studied.
value : `int`
    A digital range representation of an knowledge assessment.
"""


def get_knowledge_assessment(word_id, user_id):
    """Get or create a user rating of word knowledge.

    Get or create a user rating of word knowledge in the database.
    When creating a rating, the rating is set to "0".
    """
    if user_id and word_id:
        knowledge_assessment_obj, _ = (
            WordUserKnowledgeRelation.objects.get_or_create(
                word_id=word_id,
                user_id=user_id,
            )
        )
        knowledge_assessment = knowledge_assessment_obj.knowledge_assessment
        return knowledge_assessment


def update_word_knowledge_assessment(word_pk, user_pk, new_assessment):
    """Update the user's word knowledge score.

    Update the user's word knowledge score in the database, within the
    acceptable range.
    """
    if (MIN_KNOWLEDGE_ASSESSMENT
            <= new_assessment
            <= MAX_KNOWLEDGE_ASSESSMENT):
        WordUserKnowledgeRelation.objects.filter(
            word_id=word_pk, user_id=user_pk,
        ).update(knowledge_assessment=new_assessment)


def get_numeric_value(knowledge_assessments: str) -> list[int]:
    """Convert a string representation of a knowledge level.

    Convert a string representation of a knowledge level into a range of
    numbers for that level.
    """
    value = []
    for assessment in WORD_STUDY_ASSESSMENTS:
        if assessment in knowledge_assessments:
            value += WORD_STUDY_ASSESSMENTS[assessment]
    return value
