"""The mentorship models module."""

from django.db import models


class Mentorship(models.Model):
    """Class representing the mentor-student relationship.

    A mentor - is a user who can assign exercises to a student and view
    their solutions.
    The mentor determines the method of encouraging the student for
    completing the exercise and provides a reward for successfully
    solving the task.
    The mentor can carry out operations to write off the student's
    points when encouraging.
    """

    mentor = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='mentor',
    )
    student = models.ForeignKey(
        'CustomUser',
        on_delete=models.CASCADE,
        related_name='student',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        """Return string representation of model."""
        return f'{self.mentor} is mentor of {self.student}'

    class Meta:
        """Model settings."""

        verbose_name = 'Наставничество'
        verbose_name_plural = 'Наставничество'
        unique_together = ['mentor', 'student']


class MentorshipRequest(models.Model):
    """Request from a student to a mentor for mentorship.

    Stores the request until it is accepted or rejected.
    """

    from_user = models.ForeignKey(
        'CustomUser',
        related_name='from_student',
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        'CustomUser',
        related_name='to_mentor',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        """Return string representation of model."""
        return f'{self.from_user} sent request to {self.to_user}'

    class Meta:
        """Model settings."""

        verbose_name = 'Запрос на наставничество'
        verbose_name_plural = 'Запросы на наставничество'
        db_table = 'users_mentorship_request'
