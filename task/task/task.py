from task.task import (
    BaseSubject,
    calculation_subject,
    translate_subject,
)


class _Task:
    """
    Task class interface.

    Examples:
    ---------
    task.register_subject('subject_name', subject)
    task.apply_subject(**task_conditions)
    question_text = task.question_text
    answer_text = task.answer_text
    """

    registered_subjects = None

    def __init__(self):
        self._subject = None

    def register_subject(self, subject):
        """
        Register a subject to access it through the ``task`` object interface.
        """
        if not isinstance(subject, BaseSubject):
            raise ValueError('Not corresponding subject')
        subject_name = subject.subject_name
        self.registered_subjects = self.registered_subjects or {}
        self.registered_subjects[subject_name] = subject

    def apply_subject(self, *, subject_name, **kwargs):
        """Apply the subject for task."""
        if subject_name not in self.registered_subjects:
            raise ValueError(
                'The %s subject name is not registered' % subject_name
            )
        subject = self.registered_subjects[subject_name]
        setattr(self, '_subject', subject)
        return self._subject.apply_subject(**kwargs)

    @property
    def question_text(self):
        """Get a text representation of the task question."""
        self._check_task()
        return self._subject.question_text

    @property
    def answer_text(self):
        """Get a text representation of the task answer."""
        self._check_task()
        return self._subject.answer_text

    @property
    def info(self):
        """Get task info."""
        self._check_task()
        return self._subject.info

    def _check_task(self):
        """Check if the subject is assigned to the task."""
        if not self._subject:
            raise ValueError('The subject for the task is not specified')


task = _Task()

task.register_subject(calculation_subject)
task.register_subject(translate_subject)
