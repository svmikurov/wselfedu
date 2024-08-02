"""The mentorship models module."""

from django.db import models

from users.models import UserModel


class Mentorship(models.Model):
    """Class representing the mentor-student relationship.

    Mentor - a user who can assign tasks to a student and view his or
    her solutions to tasks.
    The mentor determines the method of encouraging the student for
    completing the exercise and provides a reward for successfully
    solving the task.
    The custodian can carry out operations to write off the student's
    points when encouraging.

    But the relationship between the mentor and the student must be
    unique.
    """

    mentor = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='mentor',
    )
    """The mentor user.
    """
    student = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='student',
    )
    """The student user.
    """

    class Meta:
        """Meta class."""

        unique_together = ['mentor', 'student']
        """The mentor-student relationship must be unique.
        """


class MentorshipRequest(models.Model):
    """Request from a student to a mentor for mentorship."""
    from_user = models.ForeignKey(
        UserModel,
        related_name='from_user',
        on_delete=models.CASCADE,
    )
    """The student user.
    """
    to_user = models.ForeignKey(
        UserModel,
        related_name='to_user',
        on_delete=models.CASCADE,
    )
    """The mentor user.
    """
