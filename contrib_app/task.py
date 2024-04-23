"""
    The module contains a common task interface for English and Mathematics
    subjects.
"""
from abc import ABC, abstractmethod
from random import randint


class _Task:
    """Task interface.

        Example:
            task.set_task_subject(subject)
            text_question = task.get_text_question()
            text_answer = task.get_text_answer()
    """

    def __init__(self):
        self._subject = None

    def set_task_subject(self, subject):
        """Set the subject for the task."""
        if not isinstance(subject, ABCSubject):
            raise ValueError('Not corresponding subject')
        self._subject = subject

    def get_text_question(self):
        """Get a text representation of the task question."""
        self._check_task()
        return self._subject.get_text_question()

    def get_text_answer(self):
        """Get a text representation of the task answer."""
        self._check_task()
        return self._subject.get_text_answer()

    def _check_task(self):
        """Check if the subject is assigned to the task."""
        if not self._subject:
            raise ValueError('The subject for the task is not specified')


task = _Task()


class ABCSubject(ABC):
    """Base subject abstract class."""

    @abstractmethod
    def set_subject_params(self, **kwargs):
        """Set subject task params."""
        pass

    @abstractmethod
    def get_text_question(self):
        """Get a text representation of the task question."""
        pass

    @abstractmethod
    def get_text_answer(self):
        """Get a text representation of the task answer."""
        pass


class _MultiplicationSubject(ABCSubject):
    """Multiplication subject task params.

        Example:
            subject = mul_subject.set_subject_params(min_number=2, max_number=8)
    """

    def __init__(self):
        self._number_range = None
        self._first_operand = None
        self._second_operand = None
        self._text_question = None
        self._text_answer = None

    def set_subject_params(self, *, min_number, max_number):
        """Set subject task params."""
        if min_number > max_number:
            raise ValueError('min_number greater than max_number')
        if not isinstance(min_number, int) or not isinstance(max_number, int):
            raise ValueError('number expected')

        self._number_range = (min_number, max_number)
        self._first_operand = self._get_random_operand_value
        self._second_operand = self._get_random_operand_value
        self._set_task_solution()

    def _get_random_operand_value(self):
        """Get random operand value."""
        return randint(*self._number_range)

    def _set_task_solution(self):
        self._text_question = f'{self._first_operand} * {self._second_operand}'
        self._text_answer = str(self._first_operand * self._second_operand)

    def get_text_question(self):
        """Get a text representation of the task question."""
        self._check_attr(self._text_question)
        return self._text_question

    def get_text_answer(self):
        """Get a text representation of the task answer."""
        self._check_attr(self._text_answer)
        return self._text_answer

    @staticmethod
    def _check_attr(attr):
        if not attr:
            raise ValueError('The subject params has not been set')


mul_subject = _MultiplicationSubject()
