"""Context processors module."""

from django.http import HttpRequest

from task.points import get_points_balance
from users.models import Mentorship


def add_student_user_data(request: HttpRequest) -> dict:
    """Add student user data to template context.

    Adds if user has mentor.
    Adds user points balance to template context.

    Parameters
    ----------
    request : `HttpRequest`
        Http request.

    Return
    ------
    context : `dict`
        Template context dictionary, may hase fields:

        - ``balance``: current user points balance (`int`).

    """
    context = {}
    user_id = request.user.id
    user_has_mentor = Mentorship.objects.filter(student=user_id).exists()

    if user_has_mentor:
        context.update(balance=get_points_balance(user_id))

    return context
