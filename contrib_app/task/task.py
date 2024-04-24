from contrib_app.task.base_subject import BaseSubject


class _Task:
    """Task class interface.

    Examples:
    ---------
    task.set_task_subject(subject)
    question_text = task.question_text
    answer_text = task.answer_text
    """

    def __init__(self):
        self._subject = None

    def set_task_subject(self, subject):
        """Set the subject for the task."""
        if not subject:
            raise ValueError('Non assigned subject')
        if not isinstance(subject, BaseSubject):
            raise ValueError('Not corresponding subject')
        self._subject = subject

    @property
    def question_text(self):
        """Get a text representation of the task question."""
        self._check_task()
        return self._subject.get_question_text()

    @property
    def answer_text(self):
        """Get a text representation of the task answer."""
        self._check_task()
        return self._subject.get_answer_text()

    def _check_task(self):
        """Check if the subject is assigned to the task."""
        if not self._subject:
            raise ValueError('The subject for the task is not specified')


task = _Task()
