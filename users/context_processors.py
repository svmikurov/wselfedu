"""User application context processors."""

from django.http import HttpRequest

from users.models import Mentorship
from users.points import get_points_balance


def add_student_user_data(request: HttpRequest) -> dict[str, float | str]:
    """Add student user data to template context.

    Adds if user has mentor.

    Adds user points balance to template context.

    :params request: Http request.
    :return: Template context dictionary, may hase fields:

     - ``balance``: current user points balance (`float` | `str`).
    """
    context = {}
    user_id = request.user.id
    user_has_mentor = Mentorship.objects.filter(student=user_id).exists()
    number_order = 100

    if user_has_mentor:
        balance = get_points_balance(user_id) / number_order
        context.update(balance=balance or '-')

    return context
