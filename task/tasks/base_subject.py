from abc import ABC, abstractmethod


class BaseSubject(ABC):
    """Subject base class."""

    _info = None

    def __init__(self):
        self._question_text = None
        self._answer_text = None

    def apply_subject(self, **kwargs):
        """Apply the subject for task."""
        self._set_task_solution()

    @abstractmethod
    def _set_task_solution(self):
        """Set up a text representation of the question and answer task.

        Override this method.
        This method should set self._question_text and self._answer_text attrs.
        """
        pass

    @abstractmethod
    def subject_name(self):
        """Get subject name.

        Override this method as property.
        """
        pass

    @property
    def question_text(self):
        """Get a text representation of the task question."""
        self._check_attr(self._question_text)
        return self._question_text

    @property
    def answer_text(self):
        """Get a text representation of the task answer."""
        self._check_attr(self._answer_text)
        return self._answer_text

    @property
    def info(self):
        return self._info

    @staticmethod
    def _check_attr(attr):
        """Check if the attribute is set."""
        if not attr:
            raise ValueError('The attribute has not been set')
