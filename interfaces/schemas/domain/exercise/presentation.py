"""Presentation exercise entity interface."""

from . import fields


class PresentationTask(
    fields.ExerciseStatusField,
    fields.QuestionTextField,
    fields.AnswerTextField,
    fields.ProgressValueField,
):
    """Presentation exercise case.

    Parameter
    ---------
    status : `ExerciseStatus`
        Current exercise status enumeration.
    question_text : `str`
        Task question text.
    answer_text : `str`
        Task answer text.
    progress_value: `int`
        Current item study progress value.

    """
