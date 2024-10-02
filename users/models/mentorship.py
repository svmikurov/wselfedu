"""The mentorship models module."""

from django.db import models

from config.constants import MENTOR, STUDENT
from users.models import UserApp


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
        UserApp,
        on_delete=models.CASCADE,
        related_name=MENTOR,
    )
    """The mentor user (`UserApp`).
    """
    student = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
        related_name=STUDENT,
    )
    """The student user (`UserApp`).
    """

    class Meta:
        """Meta class."""

        unique_together = [MENTOR, STUDENT]
        """The mentor-student relationship must be unique.
        """


class MentorshipRequest(models.Model):
    """Request from a student to a mentor for mentorship.

    Stores the request until it is accepted or rejected.
    """

    from_user = models.ForeignKey(
        UserApp,
        related_name='from_user',
        on_delete=models.CASCADE,
    )
    """The student user (`UserApp`).
    """
    to_user = models.ForeignKey(
        UserApp,
        related_name='to_user',
        on_delete=models.CASCADE,
    )
    """The mentor user (`UserApp`).
    """
