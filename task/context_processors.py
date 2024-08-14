"""Context processors module."""

from django.http import HttpRequest

from task.points import get_points_balance


def add_points_balance(request: HttpRequest) -> dict:
    """Add user points balance to template context.

    Parameters
    ----------
    request : `HttpRequest`
        Http request.

    Return
    ------
    context : `dict`
        Template context dictionary with fields:

        - ``balance``: current user points balance (`int`).
    """
    user_id = request.user.id
    balance = get_points_balance(user_id)
    context = {
        'balance': balance,
    }
    return context
