"""Context processors module."""

from django.http import HttpRequest

from task.points import get_points_balance
from users.models import Mentorship


def add_student_user_data(request: HttpRequest) -> dict[str, float | str]:
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

        - ``balance``: current user points balance (`float` | `str`).

    """
    context = {}
    user_id = request.user.id
    user_has_mentor = Mentorship.objects.filter(student=user_id).exists()

    if user_has_mentor:
        balance = get_points_balance(user_id) / 100
        context.update(balance=balance or '-')

    return context
